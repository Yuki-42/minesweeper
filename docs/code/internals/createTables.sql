CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    email TEXT NOT NULL,
    password VARCHAR(130) NOT NULL,
    username TEXT NOT NULL,
    access_level INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    key TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    time REAL
);

CREATE TABLE IF NOT EXISTS game_players (
    id SERIAL NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    winner BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);