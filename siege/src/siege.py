from __future__ import print_function

from flask import Flask, request, jsonify
from libsiege import user
from siege import util

app = Flask(__name__)

@app.route('/user', methods=['POST'])
@util.require_json
def create_user():
    data = user.create(request.get_json())
    return jsonify(data), 201


@app.route('/game', methods=['POST'])
def create_game():
    return "hello world again!\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
