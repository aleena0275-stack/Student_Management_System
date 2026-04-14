-- Student Management System Database Setup
-- Run this script in phpMyAdmin to create the database and table

-- Create the database
CREATE DATABASE IF NOT EXISTS student_db;

-- Use the database
USE student_db;

-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    subject VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data (optional)
-- INSERT INTO students (name, roll_number, subject) VALUES 
-- ('John Doe', 'R001', 'Computer Science'),
-- ('Jane Smith', 'R002', 'Mathematics'),
-- ('Mike Johnson', 'R003', 'Physics');
