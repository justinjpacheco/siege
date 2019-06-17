from flask import Flask, request, abort, jsonify
import datetime
import uuid
import json
from simplekv.fs import FilesystemStore

app = Flask(__name__)
db = FilesystemStore('./data')

# join game
@app.route('/game/<game_id>/player', methods=['POST'])
def join(game_id):
    if not request.is_json:
        response = jsonify({'message': 'i only accept json'})
        response.status_code = 400
        return response

    game_data = json.loads(db.get(game_id).decode())

    if len(game_data['players']) == 6:
        response = jsonify({'message': 'maximum amount of players reached'})
        response.status_code = 400
        return response

    game_data['players'].append(request.json)

    # save game state to database
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify(game_data)

# start the game
@app.route('/game/<game_id>/start', methods=['PATCH'])
def start(game_id):
    game_data = json.loads(db.get(game_id).decode())

    if game_data['started-at']:
        response = jsonify({'message': 'game already started'})
        response.status_code = 400
        return response

    game_data['started-at'] = datetime.datetime.now().isoformat()
    # save game state to database
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify(game_data)

# get game data
@app.route('/game/<game_id>', methods=['GET'])
def game_data(game_id):
    game_data = json.loads(db.get(game_id).decode())
    return jsonify(game_data)

# create new game
@app.route('/game', methods=['POST'])
def create():

    new_game_id = str(uuid.uuid4())
    new_game = {
        'id': new_game_id,
        'created-at': datetime.datetime.now().isoformat(),
        'started-at': False,
        'players': []
    }

    # save game state to database
    db.put(new_game_id,str.encode(json.dumps(new_game)))

    return jsonify(new_game)

# fortify position
@app.route('/game/<game_id>/territory/<territory_id>/fortify', methods=['PUT'])
def fortify():
  pass

# attack territory
@app.route('/game/<game_id>/territory/<territory_id>/attack', methods=['PUT'])
def attack():
  pass

# trade-in cards
@app.route('/game/<game_id>/cards/trade', methods=['PUT'])
def trade_in_cards():
  pass
