-- Guardian-Vault database (fresh install).
-- Run with:  mysql -u <user> -p -e "source database.sql"

CREATE DATABASE IF NOT EXISTS guardianvault CHARACTER SET utf8mb4;
USE guardianvault;

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    -- Holds a salted scrypt hash (starts with "scrypt:"), never the password itself.
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    notename VARCHAR(255) NOT NULL,
    FOREIGN KEY (userid) REFERENCES user(id)
);
