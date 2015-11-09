DROP TABLE customers;
CREATE TABLE customers
( id INTEGER PRIMARY KEY NOT NULL
, name TEXT NOT NULL UNIQUE
, email TEXT);

INSERT INTO customers (name, email)
VALUES ('Seri Resort', 'seri@gotling.se');
INSERT INTO customers (name, email)
VALUES ('Ana Warung', 'anawarung@gotling.se');
INSERT INTO customers (name, email)
VALUES ('Adeng-Adeng Bungalows', 'adeng-adeng@gotling.se');

DROP TABLE reports;
CREATE TABLE reports
( id INTEGER PRIMARY KEY NOT NULL
, customer_id INTEGER NOT NULL
, units INTEGER NOT NULL
, datetime INTEGER NOT NULL
, FOREIGN KEY(customer_id) REFERENCES customers(id));

DROP TABLE users;
CREATE TABLE users
( id INTEGER PRIMARY KEY NOT NULL
, username TEXT NOT NULL
, password TEXT
, role INTEGER NOT NULL
, customer_id INTEGER
, FOREIGN KEY(customer_id) REFERENCES customers(id));

-- ROLE: 0: admin, 1: reporter, 2: customer, 3: trash-collector, 4: money-collector

INSERT INTO users (username, role)
VALUES ('admin@e.mail', 0);

INSERT INTO users (username, role)
VALUES ('reporter@e.mail', 1);

INSERT INTO users (username, role, customer_id)
VALUES ('seri@e.mail', 2, 0);

INSERT INTO users (username, role, customer_id)
VALUES ('ana@e.mail', 2, 1);

INSERT INTO users (username, role)
VALUES ('trash@e.mail', 3);

INSERT INTO users (username, role)
VALUES ('money@e.mail', 4);