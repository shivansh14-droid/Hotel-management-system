-- ============================================
-- ROYAL STAY HOTEL MANAGEMENT SYSTEM
-- DATABASE SETUP
-- ============================================


-- ============================================
-- CREATE DATABASE
-- ============================================

CREATE DATABASE IF NOT EXISTS royal_stay_hotel;

USE royal_stay_hotel;


-- ============================================
-- 1. USERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS users (

    user_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL DEFAULT 'admin',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ============================================
-- 2. ROOMS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS rooms (

    room_id INT AUTO_INCREMENT PRIMARY KEY,

    room_number VARCHAR(10) NOT NULL UNIQUE,

    room_type VARCHAR(50) NOT NULL,

    price DECIMAL(10,2) NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'Available',

    floor INT,

    description VARCHAR(255)

);


-- ============================================
-- 3. GUESTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS guests (

    guest_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(100),

    phone VARCHAR(20),

    address VARCHAR(255),

    id_proof VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- ============================================
-- 4. BOOKINGS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS bookings (

    booking_id INT AUTO_INCREMENT PRIMARY KEY,

    guest_id INT NOT NULL,

    room_id INT NOT NULL,

    check_in DATE NOT NULL,

    check_out DATE NOT NULL,

    number_of_guests INT DEFAULT 1,

    booking_status VARCHAR(30) DEFAULT 'Confirmed',

    total_amount DECIMAL(10,2) DEFAULT 0,

    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (guest_id)
        REFERENCES guests(guest_id),

    FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)

);


-- ============================================
-- 5. PAYMENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS payments (

    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    amount DECIMAL(10,2) NOT NULL,

    payment_method VARCHAR(30) NOT NULL,

    payment_status VARCHAR(30) DEFAULT 'Paid',

    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (booking_id)
        REFERENCES bookings(booking_id)

);


-- ============================================
-- 6. STAFF TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS staff (

    staff_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(100),

    phone VARCHAR(20),

    position VARCHAR(50) NOT NULL,

    salary DECIMAL(10,2),

    joining_date DATE,

    status VARCHAR(20) DEFAULT 'Active'

);


-- ============================================
-- ADMIN USER
-- ============================================

INSERT INTO users
(username, password, role)
VALUES
('admin', 'admin123', 'admin');


-- ============================================
-- DATABASE SETUP COMPLETE
-- ============================================