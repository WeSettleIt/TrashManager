DROP TABLE customers;
CREATE TABLE customers
( id INTEGER PRIMARY KEY NOT NULL
, name TEXT NOT NULL UNIQUE
, email TEXT);

INSERT INTO customers (name, email)
VALUES ('Seri Resort', 'seri@e.mail');
INSERT INTO customers (name, email)
VALUES ('Ana Warung', 'ana@e.mail');
INSERT INTO customers (name, email)
VALUES ('Adeng-Adeng Bungalows', 'aa@e.mail');
INSERT INTO customers (name, email)
VALUES ('Tropical Hideaways', 'tropical@e.mail');

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

-- ROLE: 0: admin, 1: reports, 2: customer, 3: trash-collector, 4: money-collector

INSERT INTO users (username, role)
VALUES ('admin@e.mail', 0);

INSERT INTO users (username, role)
VALUES ('reports@e.mail', 1);

INSERT INTO users (username, role, customer_id)
VALUES ('seri@e.mail', 2, 1);

INSERT INTO users (username, role, customer_id)
VALUES ('ana@e.mail', 2, 2);

INSERT INTO users (username, role, customer_id)
VALUES ('aa@e.mail', 2, 3);

INSERT INTO users (username, role, customer_id)
VALUES ('tropical@e.mail', 2, 4);

INSERT INTO users (username, role)
VALUES ('trash@e.mail', 3);

INSERT INTO users (username, role)
VALUES ('money@e.mail', 4);