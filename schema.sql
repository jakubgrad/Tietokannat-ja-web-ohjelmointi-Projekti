CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE books (id SERIAL PRIMARY KEY, title TEXT, user_id INTEGER REFERENCES users, filename TEXT, language TEXT, author TEXT, isbn TEXT, json JSONB);
CREATE TABLE pairs (   id SERIAL PRIMARY KEY,  user_id INTEGER REFERENCES users, name TEXT,  created_at TIMESTAMP, book1_id INTEGER REFERENCES books,  book2_id INTEGER REFERENCES books );


