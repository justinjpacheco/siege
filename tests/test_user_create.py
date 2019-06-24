import pytest
import uuid
import requests
import json
from .support.assertions import assert_valid_schema

token = None

class TestSiegeApi():

    username = str(uuid.uuid4())
    password = 'password'

    def login(self):
        url = 'http://localhost:5000/login'
        headers = {'Content-Type': 'application/json'}
        data = {"username": self.username,"password": self.password}
        res = requests.get(url,data=json.dumps(data),headers=headers)
        return res

    def test_user_create(self):
        url = 'http://localhost:5000/user'
        headers = {'Content-Type': 'application/json'}
        data = {"username": self.username,"password": self.password}
        res = requests.post(url,data=json.dumps(data),headers=headers)
        json_data = res.json()

        assert res.status_code == 201
        assert_valid_schema(json_data,'new-user.json')

    def test_user_login(self):
        login_response = self.login()
        assert login_response.status_code == 200
        assert_valid_schema(login_response.json(),'login.json')

    def test_game_create(self):
        login_response = self.login()
        json_data = login_response.json()
        url = 'http://localhost:5000/game'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {0}".format(json_data['data']['token'])
        }
        res = requests.post(url,headers=headers)
        json_data = res.json()

        assert res.status_code == 201
        assert_valid_schema(json_data,'new-game.json')

        print(json_data)
