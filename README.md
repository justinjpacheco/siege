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

Status: 201 Created

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

Status: 201 Created

```json
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

If the user is already a player in the game, the response will be:

`Status: 204 No Content`

Otherwise:

`Status: 200 OK`

### Start

#### Description

Starts a game

#### Request

```
PUT /game/:game_id/start
```

#### Response


<table>
  <thead>
    <tr>
      <th>status</th>
      <th>condition</th>
      <th>return</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`200 OK`</td>
      <td>
        `successful start of the game`
      </td>
      <td>
        ```json
        {
          "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
          "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
        }
        ```
      </td>
    </tr>
    <tr>
      <td>`204 OK`</td>
      <td>
        `If the game is aready started`
      </td>
      <td>
        ```json
        {
          "id": "CD8454BC-B080-4FF4-81FB-08ECC66F1811",
          "url": "/game/CD8454BC-B080-4FF4-81FB-08ECC66F1811"
        }
        ```
      </td>
    </tr>
  </tbody>
</table>
