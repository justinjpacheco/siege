from __future__ import print_function

from flask import Flask, render_template, request
import sys
import os
import uuid
import json

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def create_user():
    users_dir = '/data/users'

    if not os.path.isdir(users_dir):
      os.mkdir(users_dir)

    user_id = str(uuid.uuid4())
    user_file = "{0}.json".format(os.path.join(users_dir,user_id))

    request_data = request.get_json()
    user_data = {
      "id": user_id,
      "username": request_data['username']
    }

    with open(user_file,"w+") as file:
      file.write(json.dumps(user_data,indent=4,sort_keys=True))

    return "user {0} created\n".format(user_id)

@app.route('/game', methods=['POST'])
def create_game():
    return "hello world again!\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
