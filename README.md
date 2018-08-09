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
status: 201 Created

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
status: 201 Created

{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
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
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811"
}
```

#### response

```
status: 200 OK

{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
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
status: 200 OK

{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
}
```
