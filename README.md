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
username | your name during the game

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
  "created_at": "2008-01-14T04:33:00Z",
  "started_at": "",
  "updated_at": "2008-01-14T04:33:00Z",
  "players": []
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
id | id of the user to be added to the game

#### example

```json
{
  "id": "10a8dcef-2cc1-4d57-b920-73a2ee830c45"
}
```

#### response

```
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "created_at": "2008-01-14T04:33:00Z",
  "started_at": "",
  "updated_at": "2008-01-14T04:34:00Z",
  "players": [
    "10a8dcef-2cc1-4d57-b920-73a2ee830c45"
  ],
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
  "created_at": "2008-01-14T04:33:00Z",
  "started_at": "2008-01-14T04:35:00Z",
  "updated_at": "2008-01-14T04:35:00Z",
  "players": [
    "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "aff254a6-2124-4362-b6b2-1e97a228bc32"
  ],
  "turn": {
    "player": "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "action": "place army"
  }
}
```

### Get

Get all information about a given game

#### Request

```
GET /game/:game_id
```

#### Response

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "created_at": "2008-01-14T04:33:00Z",
  "started_at": "2008-01-14T04:35:00Z",
  "updated_at": "2008-01-14T04:35:00Z",
  "players": [
    "10a8dcef-2cc1-4d57-b920-73a2ee830c45",
    "aff254a6-2124-4362-b6b2-1e97a228bc32"
  ],
}
```
