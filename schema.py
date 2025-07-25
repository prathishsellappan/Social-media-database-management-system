import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    try:
        # Connect to MySQL 
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = connection.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS social_media")
        cursor.execute("USE social_media")

        # Create audit_log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            audit_id INT AUTO_INCREMENT PRIMARY KEY,
            table_name VARCHAR(50) NOT NULL,
            record_id INT NOT NULL,
            action VARCHAR(50) NOT NULL,
            action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create tables with ON DELETE CASCADE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            profile_photo_url VARCHAR(255) DEFAULT 'https://picsum.photos/200',
            bio VARCHAR(255),
            email VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            caption VARCHAR(500),
            location VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            photo_id INT AUTO_INCREMENT PRIMARY KEY,
            photo_url VARCHAR(255) UNIQUE NOT NULL,
            post_id INT NOT NULL,
            photo_size INT CHECK (photo_size < 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id INT AUTO_INCREMENT PRIMARY KEY,
            video_url VARCHAR(255) UNIQUE NOT NULL,
            post_id INT NOT NULL,
            video_size INT CHECK (video_size < 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS follows (
            follower_id INT,
            followee_id INT,
            followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (follower_id, followee_id),
            FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (followee_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            user_id INT NOT NULL,
            content VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_likes (
            user_id INT NOT NULL,
            post_id INT NOT NULL,
            liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, post_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comment_likes (
            user_id INT NOT NULL,
            comment_id INT NOT NULL,
            liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, comment_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS login (
            login_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            ip VARCHAR(50) NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)

        # Create triggers for deletions
        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_user_delete
        AFTER DELETE ON users
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('users', OLD.user_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_post_delete
        AFTER DELETE ON posts
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('posts', OLD.post_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_photo_delete
        AFTER DELETE ON photos
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('photos', OLD.photo_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_video_delete
        AFTER DELETE ON videos
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('videos', OLD.video_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_follow_delete
        AFTER DELETE ON follows
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('follows', OLD.follower_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_comment_delete
        AFTER DELETE ON comments
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('comments', OLD.comment_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_post_like_delete
        AFTER DELETE ON post_likes
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('post_likes', OLD.post_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_comment_like_delete
        AFTER DELETE ON comment_likes
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('comment_likes', OLD.comment_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE TRIGGER after_login_delete
        AFTER DELETE ON login
        FOR EACH ROW
        BEGIN
            INSERT INTO audit_log (table_name, record_id, action, action_time)
            VALUES ('login', OLD.login_id, 'DELETE', NOW());
        END //
        DELIMITER ;
        """)

        # Create stored procedures
        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_user(
            IN p_username VARCHAR(50),
            IN p_email VARCHAR(50),
            IN p_profile_photo_url VARCHAR(255),
            IN p_bio VARCHAR(255)
        )
        BEGIN
            DECLARE EXIT HANDLER FOR 1062
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Username or email already exists';
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting user';
                
            INSERT INTO users (username, email, profile_photo_url, bio)
            VALUES (p_username, p_email, COALESCE(p_profile_photo_url, 'https://picsum.photos/200'), p_bio);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_post(
            IN p_user_id INT,
            IN p_caption VARCHAR(500),
            IN p_location VARCHAR(100)
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting post';
                
            INSERT INTO posts (user_id, caption, location)
            VALUES (p_user_id, p_caption, p_location);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_photo(
            IN p_post_id INT,
            IN p_photo_url VARCHAR(255),
            IN p_photo_size INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting photo';
                
            IF p_photo_size >= 5 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Photo size must be less than 5';
            END IF;
            INSERT INTO photos (post_id, photo_url, photo_size)
            VALUES (p_post_id, p_photo_url, p_photo_size);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_video(
            IN p_post_id INT,
            IN p_video_url VARCHAR(255),
            IN p_video_size INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting video';
                
            IF p_video_size >= 10 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Video size must be less than 10';
            END IF;
            INSERT INTO videos (post_id, video_url, video_size)
            VALUES (p_post_id, p_video_url, p_video_size);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_follow(
            IN p_follower_id INT,
            IN p_followee_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting follow';
                
            IF p_follower_id = p_followee_id THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User cannot follow themselves';
            END IF;
            INSERT INTO follows (follower_id, followee_id)
            VALUES (p_follower_id, p_followee_id);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_comment(
            IN p_post_id INT,
            IN p_user_id INT,
            IN p_content VARCHAR(500)
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting comment';
                
            INSERT INTO comments (post_id, user_id, content)
            VALUES (p_post_id, p_user_id, p_content);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_post_like(
            IN p_user_id INT,
            IN p_post_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting post like';
                
            INSERT INTO post_likes (user_id, post_id)
            VALUES (p_user_id, p_post_id);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_comment_like(
            IN p_user_id INT,
            IN p_comment_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting comment like';
                
            INSERT INTO comment_likes (user_id, comment_id)
            VALUES (p_user_id, p_comment_id);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE insert_login(
            IN p_user_id INT,
            IN p_ip VARCHAR(50)
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error inserting login';
                
            INSERT INTO login (user_id, ip)
            VALUES (p_user_id, p_ip);
        END //
        DELIMITER ;
        """)

        # Create delete stored procedures
        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_user(
            IN p_user_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting user';
                
            DELETE FROM users WHERE user_id = p_user_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_post(
            IN p_post_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting post';
                
            DELETE FROM posts WHERE post_id = p_post_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_photo(
            IN p_photo_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting photo';
                
            DELETE FROM photos WHERE photo_id = p_photo_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_video(
            IN p_video_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting video';
                
            DELETE FROM videos WHERE video_id = p_video_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_follow(
            IN p_follower_id INT,
            IN p_followee_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting follow';
                
            DELETE FROM follows WHERE follower_id = p_follower_id AND followee_id = p_followee_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_comment(
            IN p_comment_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting comment';
                
            DELETE FROM comments WHERE comment_id = p_comment_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_post_like(
            IN p_user_id INT,
            IN p_post_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting post like';
                
            DELETE FROM post_likes WHERE user_id = p_user_id AND post_id = p_post_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_comment_like(
            IN p_user_id INT,
            IN p_comment_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting comment like';
                
            DELETE FROM comment_likes WHERE user_id = p_user_id AND comment_id = p_comment_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE delete_login(
            IN p_login_id INT
        )
        BEGIN
            DECLARE EXIT HANDLER FOR SQLEXCEPTION
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error deleting login';
                
            DELETE FROM login WHERE login_id = p_login_id;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_most_inactive_users()
        BEGIN
            SELECT user_id, username
            FROM users
            WHERE user_id NOT IN (SELECT user_id FROM posts);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_most_liked_posts()
        BEGIN
            SELECT post_id, COUNT(*) AS like_count
            FROM post_likes
            GROUP BY post_id
            ORDER BY like_count DESC;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_avg_posts_per_user()
        BEGIN
            SELECT ROUND(COUNT(post_id) / COUNT(DISTINCT user_id), 2) AS avg_posts
            FROM posts;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_login_count_per_user()
        BEGIN
            SELECT u.user_id, u.username, COUNT(l.login_id) AS login_count
            FROM users u
            JOIN login l ON u.user_id = l.user_id
            GROUP BY u.user_id, u.username;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_users_never_commented()
        BEGIN
            SELECT user_id, username
            FROM users
            WHERE user_id NOT IN (SELECT user_id FROM comments);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_users_not_followed()
        BEGIN
            SELECT user_id, username
            FROM users
            WHERE user_id NOT IN (SELECT followee_id FROM follows);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_users_not_following()
        BEGIN
            SELECT user_id, username
            FROM users
            WHERE user_id NOT IN (SELECT follower_id FROM follows);
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_longest_captions()
        BEGIN
            SELECT user_id, caption, LENGTH(caption) AS caption_length
            FROM posts
            WHERE caption IS NOT NULL
            ORDER BY caption_length DESC
            LIMIT 5;
        END //
        DELIMITER ;
        """)

        cursor.execute("""
        DELIMITER //
        CREATE PROCEDURE get_top_posters()
        BEGIN
            SELECT u.user_id, u.username, COUNT(p.post_id) AS total_posts
            FROM users u
            LEFT JOIN posts p ON u.user_id = p.user_id
            GROUP BY u.user_id, u.username
            ORDER BY total_posts DESC
            LIMIT 5;
        END //
        DELIMITER ;
        """)

        print("Database and tables created successfully.")
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database_and_tables()