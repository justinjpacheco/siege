from .test_fixtures import *
from .support.assertions import assert_valid_schema

def test_user_create(users):
    for user in users:
        response = user['response']
        assert response.status_code == 201
        assert_valid_schema(response.json(),'new-user.json')

def test_user_auth(authed_users):
    for user in authed_users:
        response = user['response']
        assert response.status_code == 200
        assert_valid_schema(response.json(),'login.json')

def test_create_game(create_game):
    response = create_game['response']
    assert response.status_code == 201
    assert_valid_schema(response.json(),'new-game.json')

def test_join_game(join_game):
    for join in join_game:
        response = join['response']
        assert response.status_code == 200
        assert_valid_schema(response.json(),'join-game.json')

def test_start_game(start_game):
    response = start_game['response']
    assert response.status_code == 200
    assert_valid_schema(response.json(),'start-game.json')
