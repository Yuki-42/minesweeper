# Database

The database for the project will be a PostgreSQL database hosted locally on the server. The database will store all 
persistent data for the project. This includes data such as user information and game information. The database will be
accessed using the `psycopg2` library in Python through the use of the `psycopg2.extras.RealDictCursor` cursor to return
results as dictionaries. This will be wrapped in a custom `Database` class that will handle all database interactions.

## Tables

All tables in the database will have an `id` column that acts the primary key for the table. This column will be a `SERIAL`
column that auto-increments. The `id` column will be the first column in all tables.

All tables will also have a `created_at` column that will store the date and time the row was created. This column will
have a default value of `CURRENT_TIMESTAMP` and will be set to the current date and time when a new row is inserted. This
column will be the 2nd column in all tables.

### users

Used to store user information.

| Column Name | Data Type    | Default            | Description                             | Extra                | Example                              |
|-------------|--------------|--------------------|-----------------------------------------|----------------------|--------------------------------------|
| id          | SERIAL       |                    | The unique identifier for the user.     | NOT NULL PRIMARY KEY | 1                                    |
| createdAt   | TIMESTAMP    | CURRENT_TIMESTAMP  | The date and time the user was created. | NOT NULL             | 2020-01-01 12:00:00                  |
| uuid        | UUID         | uuid_generate_v4() | The UUID of the user.                   | NOT NULL             | 123e4567-e89b-12d3-a456-426614174000 |
| email       | TEXT         |                    | The email of the user.                  | NOT NULL             |                                      |
| password    | VARCHAR(130) |                    | The hashed password of the user.        | NOT NULL             |                                      |
| username    | TEXT         |                    | The username of the user.               | NOT NULL             | user                                 |
| accessLevel | INTEGER      | 0                  | The access level of the user.           | NOT NULL             | 0                                    |

```postgresql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL,
    password VARCHAR(130) NOT NULL,
    username TEXT NOT NULL,
    accessLevel INTEGER DEFAULT 0 NOT NULL
);
```
