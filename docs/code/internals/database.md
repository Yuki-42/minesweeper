# Database

The database for the project will be a PostgreSQL database hosted locally on the server. The database will store all 
persistent data for the project. This includes data such as user information and game information. The database will be
accessed using the `psycopg2` library in Python through the use of the `psycopg2.extras.RealDictCursor` cursor to return
results as dictionaries. This will be wrapped in a custom `Database` class that will handle all database interactions.

**Note:** The database relies on the `uuid-ossp` extension to generate UUIDs. This extension must be enabled in the
PostgreSQL database for the project to work.

## Tables

All tables in the database will have an `id` column that acts the primary key for the table. This column will be a `SERIAL`
column that auto-increments. The `id` column will be the first column in all tables.

All tables will also have a `created_at` column that will store the date and time the row was created. This column will
have a default value of `CURRENT_TIMESTAMP` and will be set to the current date and time when a new row is inserted. This
column will be the 2nd column in all tables.

### users

Used to store user information.

| Column Name  | Data Type    | Default            | Description                             | Extra                | Example                              |
|--------------|--------------|--------------------|-----------------------------------------|----------------------|--------------------------------------|
| id           | SERIAL       |                    | The unique identifier for the user.     | NOT NULL PRIMARY KEY | 1                                    |
| created_at   | TIMESTAMP    | CURRENT_TIMESTAMP  | The date and time the user was created. | NOT NULL             | 2020-01-01 12:00:00                  |
| uuid         | UUID         | uuid_generate_v4() | The UUID of the user.                   | NOT NULL             | 123e4567-e89b-12d3-a456-426614174000 |
| email        | TEXT         |                    | The email of the user.                  | NOT NULL             |                                      |
| password     | VARCHAR(130) |                    | The hashed password of the user.        | NOT NULL             |                                      |
| username     | TEXT         |                    | The username of the user.               | NOT NULL             | user                                 |
| access_level | INTEGER      | 0                  | The access level of the user.           | NOT NULL             | 0                                    |

```postgresql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL,
    password VARCHAR(130) NOT NULL,
    username TEXT NOT NULL,
    access_level INTEGER DEFAULT 0 NOT NULL
);
```

### games

Used to store game information.


#### Columns 

| Column Name | Data Type | Default           | Description                             | Extra                | Example             |
|-------------|-----------|-------------------|-----------------------------------------|----------------------|---------------------|
| id          | SERIAL    |                   | The unique identifier for the game.     | NOT NULL PRIMARY KEY | 1                   |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP | The date and time the game was created. | NOT NULL             | 2020-01-01 12:00:00 |
| key         | TEXT      |                   | The key to regenerate the game board.   | NOT NULL             | 1234567890abcdef    |
| width       | INTEGER   |                   | The width of the game board.            | NOT NULL             | 10                  |
| height      | INTEGER   |                   | The height of the game board.           | NOT NULL             | 10                  |
| time        | REAL      |                   | The time it took to complete the game.  |                      | 60.0                |


```postgresql
CREATE TABLE IF NOT EXISTS games (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    key TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    time REAL
);
```

### game_players

Used to store the players in a game.

| Column Name | Data Type | Default           | Description                             | Extra                | Example             |
|-------------|-----------|-------------------|-----------------------------------------|----------------------|---------------------|
| id          | SERIAL    |                   | The unique identifier for the player.   | NOT NULL PRIMARY KEY | 1                   |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP | The date and time the player was added. | NOT NULL             | 2020-01-01 12:00:00 |
| game_id     | INTEGER   |                   | The ID of the game the player is in.    | NOT NULL             | 1                   |
| user_id     | INTEGER   |                   | The ID of the user playing the game.    | NOT NULL             | 1                   |
| winner      | BOOLEAN   | FALSE             | Whether the player is the winner.       | NOT NULL             | FALSE               |

#### Keys

All keys, be they primary or foreign are listed here.

| Key Name   | Column(s) | Reference Table | Reference Column(s) |
|------------|-----------|-----------------|---------------------|
| game_id_fk | gameId    | games           | id                  |
| user_id_fk | userId    | users           | id                  |

```postgresql
CREATE TABLE IF NOT EXISTS game_players (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    winner BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
