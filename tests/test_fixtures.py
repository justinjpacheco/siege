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

    return {'users': users}

@pytest.fixture
def authed_users(users):
    url = base_url.format(path='login')
    authed_users = []

    for user in users['users']:
        data = {'username': user['username'], 'password': user['password']}
        response = requests.get(url,data=json.dumps(data),headers=headers)
        user['response'] = response
        authed_users.append(user)

    # append result to state object
    users.update({'authed_users': authed_users})
    return users

@pytest.fixture
def create_game(authed_users):

    url = base_url.format(path='game')

    # randomly find a user to create the game
    creator = authed_users['authed_users'][random.randint(0,len(authed_users) - 1)]

    # get response from authentication
    creator_response = creator['response'].json()

    # get token from response
    creator_token = creator_response['data']['token']

    # update headers with authorization
    auth = {'Authorization': "Bearer {0}".format(creator_token)}
    headers.update(auth)

    # issue request
    response = requests.post(url,headers=headers)

    # append result to state object
    authed_users.update({'create_game': response})
    return authed_users

@pytest.fixture
def join_game(create_game):

    game_data = create_game['create_game'].json()
    game_id = game_data['data']['id']
    path = 'game/{game_id}/join'.format(game_id=game_id)
    url = base_url.format(path=path)
    joined = []

    for user in create_game['authed_users']:

        # get token from auth response
        auth_data = user['response'].json()
        auth_token = auth_data['data']['token']

        # update headers with authorization
        auth = {'Authorization': "Bearer {0}".format(auth_token)}
        headers.update(auth)

        response = requests.post(url,headers=headers)
        joined.append({'response': response})

    # append result to state object
    create_game.update({'join_game': joined})
    return create_game

@pytest.fixture
def start_game(join_game):

    # get game id from game create response
    game_data = join_game['create_game'].json()
    game_id = game_data['data']['id']

    # use game id in request url
    url = base_url.format(path="game/{0}/start".format(game_id))

    # get uuid of user that created the game
    creator = None
    creator_id = game_data['data']['created-by']

    for user in join_game['authed_users']:
        user_data = user['response'].json()
        if user_data['data']['user-id'] == creator_id:
            creator = user_data
            break;

    # update headers with authorization
    auth_token = creator['data']['token']
    auth = {'Authorization': "Bearer {0}".format(auth_token)}
    headers.update(auth)

    response = requests.patch(url,headers=headers)

    # append result to state object
    join_game.update({'start_game': response})
    return join_game

@pytest.fixture
def claim_territories(start_game):

    # get game id from game create response
    game_data = start_game['start_game'].json()
    game_id = game_data['data']['id']
    claimed = []

    # territory map
    territories = {}
    for territory in game_data['data']['board']['territories']:
        territories[territory['id']] = 0

    remaining = [t for t in territories if territories[t] == 0]
    rotation = game_data['data']['rotation']

    while len(remaining):
        for user in start_game['authed_users']:

            user_data = user['response'].json()

            # find user with active turn
            active_turn = [
                r for r in rotation
                if r['turn'] is True
            ][0]

            # skip this user if it's not their turn
            if active_turn['user-id'] != user_data['data']['user-id']:
                continue

            territory = remaining[random.randint(0,len(remaining) - 1)]
            territories[territory] = 1

            # use game id in request url
            path = "game/{0}/claim/{1}".format(game_id,territory)
            url = base_url.format(path=path)

            # update headers with authorization
            auth_token = user_data['data']['token']
            auth = {'Authorization': "Bearer {0}".format(auth_token)}
            headers.update(auth)

            response = requests.put(url,headers=headers)

            # update the rotation
            rotation = response.json()['data']['rotation']

            # append to the list of claimed territories
            claimed.append({'response': response})

            # update remaining territories
            remaining = [t for t in territories if territories[t] == 0]

            if not len(remaining):
                break

    # append result to state object
    start_game.update({'claim_territories': claimed})
    return start_game

@pytest.fixture
def deploy_remaining(claim_territories):

    # get game id from game create response
    game_id = claim_territories['create_game'].json()['data']['id']
    url = base_url.format(path='game/{0}'.format(game_id))
    game_data = requests.get(url,headers=headers).json()
    rotation = game_data['data']['rotation']
    deployed = []

    # check if all remaining armies have been deployed
    deployments_remaining = [
        p for p in game_data['data']['players']
        if p['armies']['remaining'] > 0
    ]

    while len(deployments_remaining) > 0:
        for user in claim_territories['authed_users']:

            user_data = user['response'].json()

            # find user with active turn
            active_turn = [
                r for r in rotation
                if r['turn'] is True
            ][0]

            # skip this user if it's not their turn
            if active_turn['user-id'] != user_data['data']['user-id']:
                continue

            user_id = user_data['data']['user-id']

            territories = game_data['data']['board']['territories']
            owned = [
                t for t in territories
                if t['occupied-by']['user-id'] == user_id
            ]
            territory = random.choice(owned)

            player = [
                p for p in game_data['data']['players']
                if p['user-id'] == user_id
            ][0]

            data = {"armies": random.randint(0,player['armies']['remaining'])}
            path = 'game/{0}/deploy/{1}'.format(game_id,territory['id'])
            deploy_url = base_url.format(path=path)

            # update headers with authorization
            auth_token = user_data['data']['token']
            auth = {'Authorization': "Bearer {0}".format(auth_token)}
            headers.update(auth)

            response = requests.put(deploy_url,data=json.dumps(data),headers=headers)
            deployed.append({'response': response})

            # refresh game data
            game_data = requests.get(url,headers=headers).json()
            rotation = game_data['data']['rotation']

            # check if all remaining armies have been deployed
            deployments_remaining = [
                p for p in game_data['data']['players']
                if p['armies']['remaining'] > 0
            ]

            # stop if we everyone is finished deploying
            if len(deployments_remaining) == 0:
                break


    # append result to state object
    claim_territories.update({'deploy_remaining': deployed})
    return claim_territories
