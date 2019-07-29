import pytest
import uuid
import requests
import json
import random

base_url = 'http://localhost:5000/{path}'
headers = {'Content-Type': 'application/json'}

@pytest.fixture
def users():
    url = base_url.format(path='user')
    users = []

    for i in range(6):
        username = "{0}-{1}".format(i,str(uuid.uuid4()))
        password = 'password'
        data = {"username": username,"password": password}
        response = requests.post(url,data=json.dumps(data),headers=headers)

        users.append({
            'username': username,
            'password': password,
            'response': response
        })

    return users

@pytest.fixture
def authed_users(users):
    url = base_url.format(path='login')
    authed_users = []

    for user in users:
        data = {'username': user['username'], 'password': user['password']}
        response = requests.get(url,data=json.dumps(data),headers=headers)
        user['response'] = response
        authed_users.append(user)

    return authed_users

@pytest.fixture
def create_game(authed_users):

    url = base_url.format(path='game')

    # randomly find a user to create the game
    creator = authed_users[random.randint(0,len(authed_users) - 1)]

    # get response from authentication
    creator_response = creator['response'].json()

    # get token from response
    creator_token = creator_response['data']['token']

    # update headers with authorization
    auth = {'Authorization': "Bearer {0}".format(creator_token)}
    headers.update(auth)

    response = requests.post(url,headers=headers)
    return {'response': response}

@pytest.fixture
def join_game(create_game, authed_users):

    game_data = create_game['response'].json()
    game_id = game_data['data']['id']
    path = 'game/{game_id}/join'.format(game_id=game_id)
    url = base_url.format(path=path)
    joined = []

    for user in authed_users:

        # get token from auth response
        auth_data = user['response'].json()
        auth_token = auth_data['data']['token']

        # update headers with authorization
        auth = {'Authorization': "Bearer {0}".format(auth_token)}
        headers.update(auth)

        response = requests.post(url,headers=headers)
        joined.append({'response': response})

    return joined

@pytest.fixture
def start_game(authed_users, create_game, join_game):

    # get game id from game create response
    game_data = create_game['response'].json()
    game_id = game_data['data']['id']

    # use game id in request url
    url = base_url.format(path="game/{0}/start".format(game_id))

    # get uuid of user that created the game
    creator_id = game_data['data']['created-by']
    creator = None

    for user in authed_users:
        user_data = user['response'].json()
        if user_data['data']['user-id'] == creator_id:
            creator = user_data
            break;

    auth_token = creator['data']['token']

    # update headers with authorization
    auth = {'Authorization': "Bearer {0}".format(auth_token)}
    headers.update(auth)

    response = requests.patch(url,headers=headers)

    return {'response': response}

