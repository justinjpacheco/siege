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
  "started_at": null,
  "ended_at": null,
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {
    "order": [],
    "current": null,
    "action": null
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
  "position": null,
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
  "id": "cd8454bc-b080-4ff4-81fb-08ecc66f1811",
  "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811",
  "created_at": "2018-01-14T04:33:00Z",
  "started_at": "2018-01-14T04:34:00Z",
  "ended_at": null,
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {
    "order": [
      "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
      "20a8dcef-2cc1-4d57-b920-73a2ee830c45"
    ],
    "current": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "action": "place_army_on_territory"
  },
  "map": {
    "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811/map"
  },
  "players": {
    "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811/player"
  },
  "deck": {
    "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811/deck"
  },
  "history": {
    "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811/history"
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
  "id": "cd8454bc-b080-4ff4-81fb-08ecc66f1811",
  "url": "/game/cd8454bc-b080-4ff4-81fb-08ecc66f1811",
  "created_at": "2018-01-14T04:33:00Z",
  "started_at": "2018-01-14T04:34:00Z",
  "ended_at": "2018-01-14T04:35:00Z",
  "updated_at": "2018-01-14T04:35:00Z",
  "turn": {
    "order": [
      "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
      "20a8dcef-2cc1-4d57-b920-73a2ee830c45"
    ],
    "current": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "action": "place_army_on_territory"
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
  "position": null,
  "armies": {},
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
    "url": "/game/:game_id/player/10a8dcef-2cc1-4d57-b920-73a2ee830c45"
  },
  {
    "user_id": "20a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "url": "/game/:game_id/player/20a8dcef-2cc1-4d57-b920-73a2ee830c45"
  }
]
```
