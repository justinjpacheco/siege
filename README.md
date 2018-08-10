# Siege HTTP API

## User

### Create

Creates a new user

```
POST /user
```

#### input

name | description
---|---
username | display name

#### example

```json
{
  "username": "foobar"
}
```

#### response

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "username": "foobar"
}
```

## Game

### Create

Creates a new game

```
POST /game
```

#### response

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "created_at": "2018-01-14T04:33:00Z",
  "started_at": "",
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {},
  "map": {
    "url": "/game/:game_id/map"
  },
  "players": {
    "url": "/game/:game_id/player"
  },
  "deck": {
    "url": "/game/:game_id/deck"
  },
  "history": {
    "url": "/game/:game_id/history"
  }
}
```

### Join

Join an existing game

```
PUT /game/:game_id/join
```

#### input

name | description
---|---
user_id | user id of the user to be added to the game

#### example

```json
{
  "user_id": "10a8dcef-2cc1-4d57-b920-73a2ee830c45"
}
```

#### response

```json
{
  "user_id": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
  "armies": {},
  "cards": []
}
```

### Start

Starts a game

#### Request

```
PUT /game/:game_id/start
```

#### Response

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "created_at": "2018-01-14T04:33:00Z",
  "started_at": "2018-01-14T04:35:00Z",
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {
    "player": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "action": "place army"
  },
  "map": {
    "url": "/game/:game_id/map"
  },
  "players": {
    "url": "/game/:game_id/player"
  },
  "deck": {
    "url": "/game/:game_id/deck"
  },
  "history": {
    "url": "/game/:game_id/history"
  }
}
```

### Get

Get all information about a game

#### Request

```
GET /game/:game_id
```

#### Response

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "created_at": "2018-01-14T04:33:00Z",
  "started_at": "2018-01-14T04:35:00Z",
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {
    "player": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "action": "place army"
  },
  "map": {
    "url": "/game/:game_id/map"
  },
  "players": {
    "url": "/game/:game_id/player"
  },
  "deck": {
    "url": "/game/:game_id/deck"
  },
  "history": {
    "url": "/game/:game_id/history"
  }
}
```

## Player

### Player

Get information about a player in a game

#### Request

```
GET /game/:game_id/player/:player_id
```

#### Response

```json
{
  "user_id": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
  "armies": {
    "unallocated": 35
  },
  "cards": []
}
```

### Players

Get all players in a game

#### Request

```
GET /game/:game_id/player
```

#### Response

```json
[
  {
    "user_id": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "url": "/game/:game_id/player/:user_id"
  },
  {
    "user_id": "20a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "url": "/game/:game_id/player/:user_id"
  }
]
```
