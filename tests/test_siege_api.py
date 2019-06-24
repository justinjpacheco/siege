import pytest
import uuid
import requests
import json
from .support.assertions import assert_valid_schema


@pytest.fixture
def user():
    username = str(uuid.uuid4())
    password = 'password'
    url = 'http://localhost:5000/user'
    headers = {'Content-Type': 'application/json'}
    data = {"username": username,"password": password}
    res = requests.post(url,data=json.dumps(data),headers=headers)
    return {
        'creds': {'username': username, 'password': password},
        'response': res
    }

@pytest.fixture
def login(user):
    url = 'http://localhost:5000/login'
    headers = {'Content-Type': 'application/json'}
    data = {"username": user['creds']['username'],"password": user['creds']['password']}
    response = requests.get(url,data=json.dumps(data),headers=headers)
    return {'response': response}

@pytest.fixture
def game(login):
    login_data = login['response'].json()
    url = 'http://localhost:5000/game'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {0}".format(login_data['data']['token'])
    }
    response = requests.post(url,headers=headers)
    return {'response': response}

def test_user_create(user):
    assert user['response'].status_code == 201
    assert_valid_schema(user['response'].json(),'new-user.json')

def test_user_login(login):
    assert login['response'].status_code == 200
    assert_valid_schema(login['response'].json(),'login.json')

def test_game_create(game):
    assert game['response'].status_code == 201
    assert_valid_schema(game['response'].json(),'new-game.json')

def test_game_start(login, game):
    login_data = login['response'].json()
    game_data = game['response'].json()

    url = "http://localhost:5000/game/{0}/start"
    url = url.format(game_data['data']['id'])
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer {0}".format(login_data['data']['token'])
    }

    response = requests.patch(url,headers=headers)

    assert response.status_code == 200
    assert_valid_schema(response.json(),'start-game.json')
