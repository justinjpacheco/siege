import pytest
import uuid
import requests
import json
import random
from .support.assertions import assert_valid_schema


@pytest.fixture
def created_users():
    url = 'http://localhost:5000/user'
    headers = {'Content-Type': 'application/json'}
    players = []

    for p in ['a', 'b', 'c', 'd', 'e', 'f']:
        username = "{0}-{1}".format(p,str(uuid.uuid4()))
        password = 'password'
        data = {"username": username,"password": password}
        response = requests.post(url,data=json.dumps(data),headers=headers)

        players.append({
            'username': username,
            'password': password,
            'create-response': response
        })

    return players

@pytest.fixture
def authenticated_users(created_users):
    url = 'http://localhost:5000/login'
    headers = {'Content-Type': 'application/json'}

    for user in created_users:
        data = {'username': user['username'], 'password': user['password']}
        response = requests.get(url,data=json.dumps(data),headers=headers)
        user['login-response'] = response

    user_count = len(created_users)
    user_index = random.randint(0,user_count - 1)
    user = created_users[user_index]
    user['creator'] = True

    return created_users

@pytest.fixture
def created_game(authenticated_users):
    users = authenticated_users
    for user in authenticated_users:
        if 'creator' in user and user['creator'] == True:
            creator = user
    login_data = creator['login-response'].json()
    url = 'http://localhost:5000/game'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {0}".format(login_data['data']['token'])
    }

    response = requests.post(url,headers=headers)
    return {'response': response}

@pytest.fixture
def started_game(created_game, authenticated_users, join_game):
    game_data = created_game['response'].json()
    users = authenticated_users
    for user in authenticated_users:
        if 'creator' in user and user['creator'] == True:
            creator = user

    creator_login_data = creator['login-response'].json()
    creator_token = creator_login_data['data']['token']

    url = "http://localhost:5000/game/{0}/start"
    url = url.format(game_data['data']['id'])
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {0}".format(creator_token)
    }

    response = requests.patch(url,headers=headers)

    return {'response': response}

@pytest.fixture
def join_game(created_game, authenticated_users):
    joins = []
    game_data = created_game['response'].json()
    url = 'http://localhost:5000/game/{0}/join'.format(game_data['data']['id'])

    for user in authenticated_users:
        user_login_data = user['login-response'].json()
        user_auth_token = user_login_data['data']['token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {0}".format(user_auth_token)
        }
        response = requests.post(url,headers=headers)
        joins.append({'response': response})

    return joins

def test_join_game(join_game):
    for join in join_game:
        response = join['response']
        assert response.status_code == 200
        assert_valid_schema(response.json(),'join-game.json')

def test_user_create(created_users):
    for user in created_users:
        response = user['create-response']
        assert response.status_code == 201
        assert_valid_schema(response.json(),'new-user.json')

def test_user_login(authenticated_users):
    for auth_user in authenticated_users:
        response = auth_user['login-response']
        assert response.status_code == 200
        assert_valid_schema(response.json(),'login.json')

def test_game_create(created_game):
    response = created_game['response']
    assert response.status_code == 201
    assert_valid_schema(response.json(),'new-game.json')

def test_game_start(started_game):
    response = started_game['response']
    assert response.status_code == 200
    assert_valid_schema(response.json(),'start-game.json')
