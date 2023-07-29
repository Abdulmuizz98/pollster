-- A script that prepares a MySQL server for the Leads Manager project

-- Create the database ps_dev_db if it doesn't exist
CREATE DATABASE IF NOT EXISTS ps_dev_db;

-- Create the user ps_dev
CREATE USER IF NOT EXISTS'ps_dev'@'localhost' IDENTIFIED BY 'ps_dev_pwd';

-- Set privileges for user ps_dev
USE ps_dev_db;
GRANT ALL PRIVILEGES ON ps_dev_db.* TO 'ps_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ps_dev'@'localhost';

