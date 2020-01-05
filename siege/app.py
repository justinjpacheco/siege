from flask import Flask, request, redirect, abort, json, jsonify
from functools import wraps
import datetime
import hashlib
import uuid
import secrets
import random
from .board import board
from simplekv.fs import FilesystemStore

app = Flask(__name__)
db = FilesystemStore('./db')

def requires_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            response = jsonify({'message': 'i only accept json'})
            response.status_code = 400
            return response
        return f(*args, **kwargs)
    return decorated

def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' not in request.headers:
            response = jsonify({'message': 'login required'})
            response.status_code = 401
            return response

        token = request.headers['Authorization'].split(" ")[1]
        sessions = json.loads(db.get('sessions').decode())
        found = [session for session in sessions if session['token'] == token]

        if not len(found):
            response = jsonify({'message': 'login required'})
            response.status_code = 401
            return response

        return f(*args, **kwargs)
    return decorated

# user login
@app.route('/login', methods=['GET'])
@requires_json
def login():
    login_data = request.get_json()
    users = json.loads(db.get('users').decode())

    found = [
        user for user in users
        if user['username'] == login_data['username']
    ]

    if not len(found):
        response = jsonify({'message': 'user does not exists'})
        response.status_code = 400
        return response

    found_user = found[0]
    login_password_hash = hashlib.sha512(login_data['password'].encode()).hexdigest()

    if not found_user['password'] == login_password_hash:
        response = jsonify({'message': 'bad username/password'})
        response.status_code = 401
        return response

    try:
        db.get('sessions')
    except KeyError:
        print('no sessions key found. creating')
        db.put('sessions',str.encode(json.dumps([])))

    # load existing sessions
    sessions = json.loads(db.get('sessions').decode())

    # find and return previous session for user
    session = [s for s in sessions if s['user-id'] == found_user['id']]

    if len(session):
        return jsonify({"data": session[0]})

    # create new session
    session_data = {
        "user-id": found_user['id'],
        "username": found_user['username'],
        "token": secrets.token_urlsafe(),
        "issued-at": datetime.datetime.now().isoformat()
    }

    # save new session to database
    sessions.append(session_data)
    db.put('sessions',str.encode(json.dumps(sessions)))

    return jsonify({"data": session_data})

# create user
@app.route('/user', methods=['POST'])
@requires_json
def create_user():
    try:
        db.get('users')
    except KeyError:
        print('no users key found. creating')
        db.put('users',str.encode(json.dumps([])))

    user_data = request.get_json()
    users = json.loads(db.get('users').decode())

    found = [
        user for user in users
        if user['username'] == user_data['username']
    ]

    if len(found):
        response = jsonify({'message': 'user exists'})
        response.status_code = 400
        return response

    new_user = {
        "id": str(uuid.uuid4()),
        "username": user_data['username'],
        "password": hashlib.sha512(user_data['password'].encode()).hexdigest()
    }

    # save new user to database
    users.append(new_user)
    db.put('users',str.encode(json.dumps(users)))

    # remove password before returning
    new_user.pop('password')

    return jsonify({"data": new_user}), 201

# join game
@app.route('/game/<game_id>/join', methods=['POST'])
@requires_json
@requires_login
def join(game_id):

    # load game state
    game_data = json.loads(db.get(game_id).decode())

    # cannot join a started game
    if game_data['started-at']:
        response = jsonify({'message': 'cannot join started game'})
        response.status_code = 400
        return response

    # get user id from auth token
    token = request.headers['Authorization'].split(" ")[1]
    sessions = json.loads(db.get('sessions').decode())
    session = [s for s in sessions if s['token'] == token][0]
    user_id = session['user-id']

    # don't do anything if user is already in the game
    found_player = [
        player for player in game_data['players']
        if player['user-id'] == user_id
    ]

    if len(found_player):
        return jsonify({'data': game_data})

    # max 6 players allowed
    if len(game_data['players']) == 6:
        message = {'message': 'maximum amount of players reached'}
        response = jsonify(message)
        response.status_code = 400
        return response

    # append user to list of players and save game state to database
    game_data['players'].append({'user-id': user_id, 'armies': {}})
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify({'data': game_data})

# start the game
@app.route('/game/<game_id>/start', methods=['PATCH'])
@requires_login
def start_game(game_id):
    game_data = json.loads(db.get(game_id).decode())

    if game_data['started-at']:
        response = jsonify({'message': 'game already started'})
        response.status_code = 400
        return response

    if len(game_data['players']) < 3:
        response = jsonify({'message': 'minimum 3 players needed'})
        response.status_code = 400
        return response

    # get creator user id from auth token
    token = request.headers['Authorization'].split(" ")[1]
    sessions = json.loads(db.get('sessions').decode())
    session = [s for s in sessions if s['token'] == token][0]
    user_id = session['user-id']

    if game_data['created-by'] != user_id:
        response = jsonify({'message': 'cannot start game you did not create'})
        response.status_code = 400
        return response

    # populate player armies
    player_count_to_armies = {
        3: 35,
        4: 30,
        5: 25,
        6: 20
    }

    # give starting armies and determine game rotation
    armies = player_count_to_armies[len(game_data['players'])]
    for player in game_data['players']:
        player['armies']['remaining'] = armies
        game_data['rotation'].append({'user-id': player['user-id'], 'turn': False})

    # choose a random user to start
    random_user = random.choice(game_data['rotation'])
    random_user['turn'] = True

    # activate game round
    game_round = [
        gr for gr in game_data['rounds']
        if gr['id'] == 'claim-territories'
    ][0]

    game_round['started-at'] = datetime.datetime.now().isoformat()
    game_round['active'] = True

    # save game state to database
    game_data['started-at'] = datetime.datetime.now().isoformat()
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify({'data': game_data})

# get game data
@app.route('/game/<game_id>', methods=['GET'])
@requires_login
def game_data(game_id):
    game_data = json.loads(db.get(game_id).decode())
    return jsonify({'data': game_data})

# create new game
@app.route('/game', methods=['POST'])
@requires_login
def create():

    # get creator user id from auth token
    token = request.headers['Authorization'].split(" ")[1]
    sessions = json.loads(db.get('sessions').decode())
    session = [s for s in sessions if s['token'] == token][0]
    creator_user_id = session['user-id']

    # the creator of the game is the first player added
    first_player = {'user-id': creator_user_id, 'armies': {}}

    new_game_id = str(uuid.uuid4())
    new_game = {
        'id': new_game_id,
        'created-at': datetime
                        .datetime
                        .utcnow()
                        .replace(tzinfo=datetime.timezone.utc)
                        .isoformat(),
        'created-by': creator_user_id,
        'started-at': None,
        'players': [first_player],
        'rounds': [
          {
            'id': 'claim-territories',
            'started-at': None,
            'completed-at': None,
            'active': False
          },
          {
            'id': 'enforce-claimed-territories',
            'started-at': None,
            'completed-at': None,
            'active': False
          },
          {
            'id': 'main',
            'started-at': None,
            'completed-at': None,
            'active': False
          },
        ],
        'rotation': [],
        'history': [],
        'board': board()
    }

    # save game state to database
    db.put(new_game_id,str.encode(json.dumps(new_game)))

    return jsonify({'data': new_game}), 201

# claim territory
@app.route('/game/<game_id>/claim/<territory_id>', methods=['PUT'])
@requires_login
def claim(game_id,territory_id):

    game_data = json.loads(db.get(game_id).decode())

    # get user id from auth token and session db
    token = request.headers['Authorization'].split(" ")[1]
    sessions = json.loads(db.get('sessions').decode())
    session = [s for s in sessions if s['token'] == token][0]
    user_id = session['user-id']

    # check if user is in the game
    player = [p for p in game_data['players'] if p['user-id'] == user_id]
    if not len(player):
        response = jsonify({'message': 'user not in game'})
        response.status_code = 400
        return response

    player = player[0]

    # check current game round is correct
    current_game_round = [
        gr for gr in game_data['rounds']
        if gr['active'] is True
    ][0]

    if current_game_round['id'] != 'claim-territories':
        response = jsonify({'message': 'wrong game round'})
        response.status_code = 400
        return response

    # check if this is the players turn
    rotation = [
        r for r in game_data['rotation']
        if r['turn'] is True and r['user-id'] == user_id
    ]
    if not len(rotation):
        response = jsonify({'message': 'incorrect turn order'})
        response.status_code = 400
        return response

    # try to locate territory
    territories = game_data['board']['territories']
    territory = [
        t for t in territories
        if t['id'] == territory_id
    ]

    # check if territory exists
    if not len(territory):
        response = jsonify({'message': 'territory does not exist'})
        response.status_code = 400
        return response

    territory = territory[0]

    # check if territory is unoccupied
    if territory['occupied-by']['user-id'] is not None:
        response = jsonify({'message': 'territory is occupied'})
        response.status_code = 400
        return response

    # claim territory
    territory['occupied-by'].update({'armies': 1, 'user-id': user_id})

    # remove 1 army from player
    player['armies']['remaining'] -= 1

    # update the rotation to the next player
    for i, r in enumerate(game_data['rotation']):
        if r['turn'] is True:
            if i == len(game_data['rotation']) - 1:
                game_data['rotation'][0]['turn'] = True
            else:
                game_data['rotation'][i+1]['turn'] = True
            r['turn'] = False
            break

    # check if all territories have been claimed
    remaining = [t for t in territories if t['occupied-by']['user-id'] is None]
    if len(remaining) == 0:
        current_game_round['completed-at'] = datetime.datetime.now().isoformat()
        current_game_round['active'] = False

        # next game round
        next_game_round = [
            gr for gr in game_data['rounds']
            if gr['id'] == 'enforce-claimed-territories'
        ][0]
        next_game_round['started-at'] = datetime.datetime.now().isoformat()
        next_game_round['active'] = True

    # save game state to database
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify({'data': game_data})

# deploy armies to position
@app.route('/game/<game_id>/deploy/<territory_id>', methods=['PUT'])
@requires_json
def deploy(game_id,territory_id):
    game_data = json.loads(db.get(game_id).decode())

    # get user id from auth token and session db
    token = request.headers['Authorization'].split(" ")[1]
    sessions = json.loads(db.get('sessions').decode())
    session = [s for s in sessions if s['token'] == token][0]
    user_id = session['user-id']

    # check if user is in the game
    player = [p for p in game_data['players'] if p['user-id'] == user_id]
    if not len(player):
        response = jsonify({'message': 'user not in game'})
        response.status_code = 400
        return response

    player = player[0]

    # check current game round is correct
    current_game_round = [
        gr for gr in game_data['rounds']
        if gr['active'] is True
    ][0]

    if current_game_round['id'] != 'enforce-claimed-territories':
        response = jsonify({'message': 'wrong game round'})
        response.status_code = 400
        return response

    # check if this is the players turn
    rotation = [
        r for r in game_data['rotation']
        if r['turn'] is True and r['user-id'] == user_id
    ]
    if not len(rotation):
        response = jsonify({'message': 'incorrect turn order'})
        response.status_code = 400
        return response

    # try to locate territory
    territories = game_data['board']['territories']
    territory = [
        t for t in territories
        if t['id'] == territory_id
    ]

    # check if territory exists
    if not len(territory):
        response = jsonify({'message': 'territory does not exist'})
        response.status_code = 400
        return response

    territory = territory[0]

    # check if territory is occupied by user
    if territory['occupied-by']['user-id'] != user_id:
        response = jsonify({'message': 'you do not occupy this territory'})
        response.status_code = 400
        return response

    # get request data
    deploy_data = request.get_json()
    armies = deploy_data['armies']

    # update territory
    territory['occupied-by'].update({'armies': armies})

    # remove armies from player
    player['armies']['remaining'] -= armies

    # update the rotation to the next player
    for i, r in enumerate(game_data['rotation']):
        if r['turn'] is True:
            if i == len(game_data['rotation']) - 1:
                game_data['rotation'][0]['turn'] = True
            else:
                game_data['rotation'][i+1]['turn'] = True
            r['turn'] = False
            break

    # check if all remaining armies have been deployed
    deployments_remaining = [
        p for p in game_data['players']
        if p['armies']['remaining'] > 0
    ]
    if len(deployments_remaining) == 0:
        current_game_round['completed-at'] = datetime.datetime.now().isoformat()
        current_game_round['active'] = False

        # next game round
        next_game_round = [
            gr for gr in game_data['rounds']
            if gr['id'] == 'main'
        ][0]
        next_game_round['started-at'] = datetime.datetime.now().isoformat()
        next_game_round['active'] = True

    # save game state to database
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify({'data': game_data})

# trade-in cards
@app.route('/game/<game_id>/cards/trade', methods=['PUT'])
def trade_in_cards():
  pass
