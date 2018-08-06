# Siege HTTP API

## User

### Create

Creates a new user

```
POST /api/v1/user
```

#### input

name | description
---|---
username | your name during the game


#### example

```json
{
  "username": "general zod"
}
```

#### response

status: 201 Created

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811"
}
```

## Game

### Create

Creates a new game

```
POST /api/v1/game
```

```json
{
  "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
  "url": "/api/v1/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
}
```

### Join

Joins an existing game
