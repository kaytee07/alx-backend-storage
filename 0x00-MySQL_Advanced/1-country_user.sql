-- script that create a table of users
CREATE TABLE IF NOT EXISTS users (
id INT NOT NULL AUTO_INCREMENT AND PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
name VARCHAR(255),
country CHAR(2) NOT NULL DEFAULT 'US' CHECK (country IN ('US', 'CO', 'TN'))
);