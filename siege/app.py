from flask import Flask, request, redirect, abort, json, jsonify
from functools import wraps
import datetime
import hashlib
import uuid
import secrets
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

    found = [user for user in users if user['username'] == login_data['username']]

    if not len(found):
        print(found)
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

    found = [user for user in users if user['username'] == user_data['username']]

    if len(found):
        print(found)
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
    game_data = json.loads(db.get(game_id).decode())

    if len(game_data['players']) == 6:
        response = jsonify({'message': 'maximum amount of players reached'})
        response.status_code = 400
        return response

    game_data['players'].append(request.json)

    # save game state to database
    db.put(game_id,str.encode(json.dumps(game_data)))

    return jsonify({'data': game_data})

# start the game
@app.route('/game/<game_id>/start', methods=['PATCH'])
@requires_login
def start(game_id):
    game_data = json.loads(db.get(game_id).decode())

    if game_data['started-at']:
        response = jsonify({'message': 'game already started'})
        response.status_code = 400
        return response

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
    user_id = session['user-id']

    # the creator of the game is the first player added
    first_player = {'id': session['user-id']}

    new_game_id = str(uuid.uuid4())
    new_game = {
        'id': new_game_id,
        'created-at': datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
        'created-by': user_id,
        'started-at': None,
        'players': [first_player]
    }

    print(new_game)

    # save game state to database
    db.put(new_game_id,str.encode(json.dumps(new_game)))

    return jsonify({'data': new_game}), 201

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
