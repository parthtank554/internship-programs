-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS story_share;

USE story_share;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT '/media/default-profile.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS story (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    media_url VARCHAR(255) NOT NULL,
    media_type ENUM('image', 'video') NOT NULL,
    duration INT DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS story_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (user_id, story_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (story_id) REFERENCES story(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS story_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (user_id, story_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (story_id) REFERENCES story(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS story_replies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    reply_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (story_id) REFERENCES story(id) ON DELETE CASCADE
);

-- Create stored procedures
DELIMITER //

-- Register User
CREATE PROCEDURE IF NOT EXISTS RegisterUser(IN p_username VARCHAR(50), IN p_email VARCHAR(100), IN p_password VARCHAR(255), IN p_full_name VARCHAR(100))
BEGIN
    INSERT INTO users (username, email, password, full_name) VALUES (p_username, p_email, p_password, p_full_name);
    SELECT LAST_INSERT_ID() AS user_id;
END //

-- Get User By Username
CREATE PROCEDURE IF NOT EXISTS GetUserByUsername(IN p_username VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE username = p_username;
END //

-- Get User By Email
CREATE PROCEDURE IF NOT EXISTS GetUserByEmail(IN p_email VARCHAR(100))
BEGIN
    SELECT * FROM users WHERE email = p_email;
END //

-- Get User By ID
CREATE PROCEDURE IF NOT EXISTS GetUserById(IN p_id INT)
BEGIN
    SELECT * FROM users WHERE id = p_id;
END //

-- Update User Profile
CREATE PROCEDURE IF NOT EXISTS UpdateUserProfile(IN p_id INT, IN p_full_name VARCHAR(100), IN p_profile_pic VARCHAR(255))
BEGIN
    UPDATE users SET full_name = p_full_name, profile_pic = p_profile_pic WHERE id = p_id;
END //

-- Create Story
CREATE PROCEDURE IF NOT EXISTS CreateStory(IN p_user_id INT, IN p_media_url VARCHAR(255), IN p_media_type ENUM('image', 'video'), IN p_duration INT)
BEGIN
    INSERT INTO story (user_id, media_url, media_type, duration) VALUES (p_user_id, p_media_url, p_media_type, p_duration);
    SELECT LAST_INSERT_ID() AS story_id;
END //

-- Get Active Stories
CREATE PROCEDURE IF NOT EXISTS GetActiveStories()
BEGIN
    SELECT s.*, u.username, u.profile_pic 
    FROM story s 
    JOIN users u ON s.user_id = u.id 
    WHERE s.created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR) 
    ORDER BY s.created_at DESC;
END //

-- Get User Stories
CREATE PROCEDURE IF NOT EXISTS GetUserStories(IN p_user_id INT)
BEGIN
    SELECT s.*, u.username, u.profile_pic 
    FROM story s 
    JOIN users u ON s.user_id = u.id 
    WHERE s.user_id = p_user_id 
    ORDER BY s.created_at DESC;
END //

-- Get Story Details
CREATE PROCEDURE IF NOT EXISTS GETSTORYDETAILS(IN p_story_id INT)
BEGIN
    SELECT s.*, u.username, u.profile_pic 
    FROM story s 
    JOIN users u ON s.user_id = u.id 
    WHERE s.id = p_story_id;
END //

-- Add Story View
CREATE PROCEDURE IF NOT EXISTS ADD_STORY_VIEW(IN p_user_id INT, IN p_story_id INT)
BEGIN
    INSERT IGNORE INTO story_views (user_id, story_id) VALUES (p_user_id, p_story_id);
END //

DELIMITER ;