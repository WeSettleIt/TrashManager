CREATE TABLE customers
( id INTEGER PRIMARY KEY NOT NULL
, name TEXT NOT NULL UNIQUE
, email TEXT UNIQUE);

INSERT INTO customers (name, email)
VALUES ('Seri Resort', 'seri@gotling.se');
INSERT INTO customers (name, email)
VALUES ('Ana Warung', 'anawarung@gotling.se');
INSERT INTO customers (name, email)
VALUES ('Adeng-Adeng Bungalows', 'adeng-adeng@gotling.se');

CREATE TABLE reports
( id INTEGER PRIMARY KEY NOT NULL
, customer_id INTEGER
, units INTEGER
, datetime INTEGER
, FOREIGN KEY(customer_id) REFERENCES customers(id));