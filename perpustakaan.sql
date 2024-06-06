CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE penulis (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE kategori (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    publish_date DATE NOT NULL DEFAULT CURRENT_DATE,
    copies_available INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES penulis(id),
    CONSTRAINT fk_category FOREIGN KEY(category_id) REFERENCES kategori(id)
);

CREATE TABLE transaction_book (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    return_date DATE,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(id)
);

CREATE TABLE return_book (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    return_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_returned_book FOREIGN KEY(book_id) REFERENCES books(id)
);
