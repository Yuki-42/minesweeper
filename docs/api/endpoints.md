# Endpoints

## Base URL

The base URL for the API is `http://localhost:3000/api/`.

The base URL can be interacted with using the `OPTIONS` or `GET` methods to get information about the API.

`OPTIONS /api/` -> Get information about the API.
`GET /api/` -> Get information about the API.

Note: No payload is required for these requests. If a payload is provided, it will be ignored.

## Game

The game endpoint is used to interact with all game-related data. The following endpoints are available:

Most functions of the game endpoint require a valid JWT token to be provided in the `Authorization` header. The token must be in the format `Bearer
<token>`.
The token can be obtained by logging in or registering a new user.

Most common functions relating to games are handled on this endpoint using specific HTTP methods.

### Endpoints

#### GET /api/game/

Get a specific game by ID.

##### Parameters

- `gid`: The ID of the game to get.
- `uid`: The ID of the user to get games for.

##### Response

- `200 OK`: Returns the game.
- `400 Bad Request`: If the request is malformed.
- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the user is forbidden from viewing the game.
- `404 Not Found`: If the game or user is not found.

#### GET /api/games/

Get a list of all games. 

- `all`: Get all games.
- `active`: Get all active games.
- `completed`: Get all completed games.
- `user`: Get all games for the current user.
- `game`: Get a specific game by ID.

##### Parameters

- `type`: The type of games to get. Can be one of `all`, `active`, or `completed`. Default is `all`.

##### Response

- `200 OK`: Returns a list of games.
- `400 Bad Request`: If the request is malformed.
- `401 Unauthorized`: If the user is not authenticated.
- `403 Forbidden`: If the user is forbidden from viewing the game.
- `404 Not Found`: If the game or user is not found.

##### Example

