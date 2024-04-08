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

All data that is accessed by the API must have a `uuid` column that will store a UUID for the row. This column will have a
default value of `uuid_generate_v4()` and will be set to a new UUID when a new row is inserted. This column will be the
3rd column in all tables. This UUID will be used to identify the row in the API.

## Many to Many Relationships

Some tables will have many-to-many relationships. These relationships will be handled using a separate table that will
store the IDs of the two tables that are related. These tables will comply with the naming convention of `table1_table2`
where `table1` and `table2` are the names of the tables that are related. These tables will also comply with the above [rules](#tables).

The foreign keys in these tables must be set to `ON DELETE CASCADE` and `ON UPDATE CASCADE` to ensure that when a row is deleted from one of the
related tables, the row is also deleted from the relationship table.

The foreign keys must also follow the naming convention of `table1_id` and `table2_id` where `table1` and `table2` are the names of the tables that are related.

### users

Used to store user information.

| Column Name   | Data Type    | Default            | Description                             | Extra                | Example                              |
|---------------|--------------|--------------------|-----------------------------------------|----------------------|--------------------------------------|
| id            | SERIAL       |                    | The unique identifier for the user.     | NOT NULL PRIMARY KEY | 1                                    |
| created_at    | TIMESTAMP    | CURRENT_TIMESTAMP  | The date and time the user was created. | NOT NULL             | 2020-01-01 12:00:00                  |
| uuid          | UUID         | uuid_generate_v4() | The UUID of the user.                   | NOT NULL             | 123e4567-e89b-12d3-a456-426614174000 |
| email         | TEXT         |                    | The email of the user.                  | NOT NULL             |                                      |
| password      | VARCHAR(130) |                    | The hashed password of the user.        | NOT NULL             |                                      |
| username      | TEXT         |                    | The username of the user.               | NOT NULL             | user                                 |
| access_level  | INTEGER      | 0                  | The access level of the user.           | NOT NULL             | 0                                    |
| access_token  | TEXT         |                    | The access token of the user.           | NOT NULL             |                                      |
| oauth_scopes  | TEXT[]       |                    | The OAuth scopes of the user.           |                      |                                      |

```postgresql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL,
    password VARCHAR(130) NOT NULL,
    username TEXT NOT NULL,
    access_level INTEGER DEFAULT 0 NOT NULL,
    access_token TEXT NOT NULL,
    oauth_scopes TEXT[]
);
```

### tokens

Used to store access tokens for users.

| Column Name | Data Type | Default           | Description                              | Extra                | Example             |
|-------------|-----------|-------------------|------------------------------------------|----------------------|---------------------|
| id          | SERIAL    |                   | The unique identifier for the token.     | NOT NULL PRIMARY KEY | 1                   |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP | The date and time the token was created. | NOT NULL             | 2020-01-01 12:00:00 |
| user_id     | INTEGER   |                   | The ID of the user the token is for.     | NOT NULL             | 1                   |
| token       | TEXT      |                   | The access token.                        | NOT NULL             | Token               |
| expires_at  | TIMESTAMP |                   | The date and time the token expires.     | NOT NULL             | 2020-01-01 12:00:00 |

#### Keys

| Key Name   | Column(s) | Reference Table | Reference Column(s) |
|------------|-----------|-----------------|---------------------|
| user_id_fk | user_id   | users           | id                  |

#### SQL

```postgresql
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);
```

### games

Used to store game information.


#### Columns 

| Column Name | Data Type | Default            | Description                             | Extra                | Example                              |
|-------------|-----------|--------------------|-----------------------------------------|----------------------|--------------------------------------|
| id          | SERIAL    |                    | The unique identifier for the game.     | NOT NULL PRIMARY KEY | 1                                    |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP  | The date and time the game was created. | NOT NULL             | 2020-01-01 12:00:00                  |
| uuid        | UUID      | uuid_generate_v4() | The UUID of the game.                   | NOT NULL             | 123e4567-e89b-12d3-a456-426614174000 |
| key         | TEXT      |                    | The key to regenerate the game board.   | NOT NULL             | 1234567890abcdef                     |
| width       | INTEGER   |                    | The width of the game board.            | NOT NULL             | 10                                   |
| height      | INTEGER   |                    | The height of the game board.           | NOT NULL             | 10                                   |
| time        | REAL      |                    | The time it took to complete the game.  |                      | 60.0                                 |


```postgresql
CREATE TABLE IF NOT EXISTS games (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    key TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    time REAL
);
```

### games_users

Used to store the users in a game.

| Column Name | Data Type | Default           | Description                             | Extra                | Example             |
|-------------|-----------|-------------------|-----------------------------------------|----------------------|---------------------|
| id          | SERIAL    |                   | The unique identifier for the player.   | NOT NULL PRIMARY KEY | 1                   |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP | The date and time the player was added. | NOT NULL             | 2020-01-01 12:00:00 |
| game_id     | INTEGER   |                   | The ID of the game the player is in.    | NOT NULL             | 1                   |
| user_id     | INTEGER   |                   | The ID of the user playing the game.    | NOT NULL             | 1                   |
| winner      | BOOLEAN   | FALSE             | Whether the player is the winner.       | NOT NULL             | FALSE               |

#### Keys


| Key Name   | Column(s) | Reference Table | Reference Column(s) |
|------------|-----------|-----------------|---------------------|
| game_id_fk | games_id  | games           | id                  |
| user_id_fk | users_id  | users           | id                  |

#### SQL

```postgresql
CREATE TABLE IF NOT EXISTS games_users (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    games_id INTEGER NOT NULL,
    users_id INTEGER NOT NULL,
    winner BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (games_id) REFERENCES games(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (games_id, users_id)  /* Prevent duplicate entries */
);
```

### logs

Used to store logs for the application.

| Column Name | Data Type | Default           | Description                            | Extra                | Example             |
|-------------|-----------|-------------------|----------------------------------------|----------------------|---------------------|
| id          | SERIAL    |                   | The unique identifier for the log.     | NOT NULL PRIMARY KEY | 1                   |
| created_at  | TIMESTAMP | CURRENT_TIMESTAMP | The date and time the log was created. | NOT NULL             | 2020-01-01 12:00:00 |
| level       | INTEGER   |                   | The log level.                         | NOT NULL             | 0                   |
| module      | TEXT      |                   | The module that generated the log.     | NOT NULL             | api                 |
| message     | TEXT      |                   | The log message.                       | NOT NULL             | Log message         |

#### SQL

```postgresql
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    level INTEGER NOT NULL,
    module TEXT NOT NULL,
    message TEXT NOT NULL
);
```
