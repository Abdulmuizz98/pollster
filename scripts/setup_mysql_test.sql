-- A script that prepares a test MySQL server for the Leads Manager project

-- Create the database ps_test_db if it doesn't exist
CREATE DATABASE IF NOT EXISTS ps_test_db;

-- Create the user ps_test
CREATE USER IF NOT EXISTS'ps_test'@'localhost' IDENTIFIED BY 'ps_test_pwd';

-- Set privileges for user ps_test
USE ps_test_db;
GRANT ALL PRIVILEGES ON ps_test_db.* TO 'ps_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ps_test'@'localhost';

