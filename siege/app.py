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
    found_player = [player for player in game_data['players'] if player['id'] == user_id]
    if len(found_player):
        return jsonify({'data': game_data})

    # max 6 players allowed
    if len(game_data['players']) == 6:
        message = {'message': 'maximum amount of players reached'}
        response = jsonify(message)
        response.status_code = 400
        return response

    # append user to list of players and save game state to database
    game_data['players'].append({'id': user_id, 'armies': {}})
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
        game_data['rotation'].append({'player-id': player['id'], 'turn': False})

    # set game round
    game_data['round'] = 'SETUP-ROUND-1'

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
    first_player = {'id': user_id, 'armies': {}}

    new_game_id = str(uuid.uuid4())
    new_game = {
        'id': new_game_id,
        'created-at': datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
        'created-by': user_id,
        'started-at': None,
        'players': [first_player],
        'rotation': [],
        'history': [],
        'board': []
    }

    # save game state to database
    db.put(new_game_id,str.encode(json.dumps(new_game)))

    return jsonify({'data': new_game}), 201

# capture territory
@app.route('/game/<game_id>/capture/<territory_id>', methods=['PUT'])
def attack():
  pass

# fortify position
@app.route('/game/<game_id>/territory/<territory_id>/fortify', methods=['PUT'])
def fortify():
  pass

# trade-in cards
@app.route('/game/<game_id>/cards/trade', methods=['PUT'])
def trade_in_cards():
  pass

def board():
    continents = [
        {'id': 'asia', 'name': 'asia', 'bonus': 7},
        {'id': 'north-america', 'name': 'north america', 'bonus': 5},
        {'id': 'europe', 'name': 'europe', 'bonus': 5},
        {'id': 'africa', 'name': 'africa', 'bonus': 3},
        {'id': 'australia', 'name': 'australia', 'bonus': 2},
        {'id': 'south-america', 'name': 'south america', 'bonus': 2},
    ]
    territories = [
        {
            'id': 'alaska',
            'name': 'alaska',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' ['alberta', 'north-west-territory', 'kamchatka']
        },
        {
            'id': 'north-west-territory',
            'name': 'north west territory',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' ['alberta', 'alaska', 'ontario', 'greenland']
        },
        {
            'id': 'greenland',
            'name': 'greenland',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'north-west-territory',
                'quebec',
                'ontario',
                'iceland'
            ]
        },
        {
            'id': 'alberta',
            'name': 'alberta',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'north-west-territory',
                'alaska',
                'ontario',
                'western-united-states'
            ]
        },
        {
            'id': 'ontario',
            'name': 'ontario',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'north-west-territory',
                'alberta',
                'quebec',
                'greenland',
                'western-united-states',
                'eastern-united-states'
            ]
        },
        {
            'id': 'quebec',
            'name': 'quebec',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'ontario',
                'greenland',
                'eastern-united-states'
            ]
        },
        {
            'id': 'western-united-states',
            'name': 'western united states',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'alberta',
                'ontario',
                'eastern-united-states',
                'central-america'
            ]
        },
        {
            'id': 'eastern-united-states',
            'name': 'western united states',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'quebec',
                'ontario',
                'western-united-states',
                'central-america'
            ]
        },
        {
            'id': 'central-america',
            'name': 'central america',
            'continent': 'north-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'eastern-united-states',
                'western-united-states',
                'venezuela'
            ]
        },
        {
            'id': 'venezuela',
            'name': 'venezuela',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'central-america',
                'peru',
                'brazil'
            ]
        },
        {
            'id': 'peru',
            'name': 'peru',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'venezuela',
                'brazil',
                'argentina',
            ]
        },
        {
            'id': 'brazil',
            'name': 'brazil',
            'continent': 'south-america',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'venezuela',
                'peru',
                'argentina',
                'north-africa',
            ]
        },
        {
            'id': 'north-africa',
            'name': 'north africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'brazil',
                'western-europe',
                'southern-europe',
                'egypt',
                'east-africa',
                'congo',
            ]
        },
        {
            'id': 'egypt',
            'name': 'egypt',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'north-africa',
                'southern-europe',
                'middle-east',
                'east-africa',
            ]
        },
        {
            'id': 'east-africa',
            'name': 'east africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'middle-east',
                'egypt',
                'north-africa',
                'congo',
                'south-africa',
                'madagascar',
            ]
        },
        {
            'id': 'congo',
            'name': 'congo',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'north-africa',
                'east-africa',
                'south-africa',
            ]
        },
        {
            'id': 'south-africa',
            'name': 'south africa',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'congo',
                'east-africa',
                'madagascar',
            ]
        },
        {
            'id': 'madagascar',
            'name': 'madagascar',
            'continent': 'africa',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'east-africa',
                'south-africa',
            ]
        },
        {
            'id': 'iceland',
            'name': 'iceland',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'greenland',
                'great-britain',
                'scandinavia',
            ]
        },
        {
            'id': 'scandinavia',
            'name': 'scandinavia',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'ukraine',
                'northern-europe',
                'iceland',
                'great-britain',
            ]
        },
        {
            'id': 'ukraine',
            'name': 'ukraine',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'ural',
                'afghanistan',
                'middle-east',
                'southern-europe',
                'northern-europe',
                'scandinavia',
            ]
        },
        {
            'id': 'northern-europe',
            'name': 'northern europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'scandinavia',
                'ukraine',
                'southern-europe',
                'western-europe',
                'great-britain',
            ]
        },
        {
            'id': 'southern-europe',
            'name': 'southern europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'middle-east',
                'egypt',
                'north-africa',
                'western-europe',
                'northern-europe',
                'ukraine',
            ]
        },
        {
            'id': 'western-europe',
            'name': 'western europe',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'great-britain',
                'northern-europe',
                'southern-europe',
                'north-africa',
            ]
        },
        {
            'id': 'great-britain',
            'name': 'great britain',
            'continent': 'europe',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'iceland',
                'scandinavia',
                'northern-europe',
                'western-europe',
            ]
        },
        {
            'id': 'indonesia',
            'name': 'indonesia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'siam',
                'new-guinea',
                'western-australia',
            ]
        },
        {
            'id': 'new-guinea',
            'name': 'new guinea',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'indonesia',
                'new-guinea',
                'western-australia',
                'eastern-australia',
            ]
        },
        {
            'id': 'western-australia',
            'name': 'western australia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'indonesia',
                'new-guinea',
                'eastern-australia',
            ]
        },
        {
            'id': 'eastern-australia',
            'name': 'eastern australia',
            'continent': 'australia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'new-guinea',
                'eastern-australia',
                'western-australia',
            ]
        },
        {
            'id': 'middle-east',
            'name': 'middle east',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'east-africa',
                'egypt',
                'southern-europe',
                'ukraine',
                'afghanistan',
                'india',
            ]
        },
        {
            'id': 'afghanistan',
            'name': 'afghanistan',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'middle-east',
                'ukraine',
                'ural',
                'china',
                'india',
            ]
        },
        {
            'id': 'ural',
            'name': 'ural',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'afghanistan',
                'ukraine',
                'siberia',
                'china',
            ]
        },
        {
            'id': 'siberia',
            'name': 'siberia',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'ural',
                'china',
                'yakutsk',
                'irkutsk',
                'mongolia',
                'china',
            ]
        },
        {
            'id': 'yakutsk',
            'name': 'yakutsk',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'kamchatka',
                'irkutsk',
                'siberia',
            ]
        },
        {
            'id': 'kamchatka',
            'name': 'kamchatka',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'yakutsk',
                'irkutsk',
                'mongolia',
                'japan',
            ]
        },
        {
            'id': 'japan',
            'name': 'japan',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'kamchatka',
                'mongolia',
            ]
        },
        {
            'id': 'irkutsk',
            'name': 'irkutsk',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'siberia',
                'yakutsk',
                'kamchatka',
                'mongolia',
            ]
        },
        {
            'id': 'mongolia',
            'name': 'mongolia',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'siberia',
                'irkutsk',
                'kamchatka',
                'japan',
                'china',
            ]
        },
        {
            'id': 'china',
            'name': 'china',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'mongolia',
                'siberia',
                'ural',
                'afghanistan',
                'india',
                'siam',
            ]
        },
        {
            'id': 'siam',
            'name': 'siam',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'china',
                'india',
                'indonesia',
            ]
        },
        {
            'id': 'india',
            'name': 'india',
            'continent': 'asia',
            'occupied-by': {'user-id': None, 'armies': None},
            'adjacent-to' [
                'middle-east',
                'afghanistan',
                'china',
                'siam',
            ]
        },
    ]

    return {'continents': continents, 'territories': territories}
