/* Drop existing tables */
DROP TABLE IF EXISTS game_players;  /* Tables are dropped in order of dependency */
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS tokens;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS logs;

/* Add uuid extension */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* Create tables */
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

CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    key TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    time REAL
);

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

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    level INTEGER NOT NULL,
    module TEXT NOT NULL,
    message TEXT NOT NULL
);

/* Add permissions */
GRANT ALL PRIVILEGES ON SCHEMA public TO minesweeper;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO minesweeper;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO minesweeper;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO minesweeper;
