-- init.sql
-- Script de inicialización para MySQL en Docker

CREATE DATABASE IF NOT EXISTS guestbook_db;
USE guestbook_db;

-- Create a specific user account for the guestbook application
CREATE USER 'guestbook_user'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';

-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS guestbook_db;

-- Grant specific permissions ONLY for the guestbook_db database
GRANT SELECT, INSERT, CREATE ON guestbook_db.* TO 'guestbook_user'@'localhost';

-- Update privileges
FLUSH PRIVILEGES;