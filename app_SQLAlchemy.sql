CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(28) NOT NULL UNIQUE,
    public_id UUID NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    public_id UUID NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(28) NOT NULL UNIQUE,
    public_id UUID NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    public_id UUID NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id)
);

