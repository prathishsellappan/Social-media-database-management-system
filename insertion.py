import mysql.connector
from mysql.connector import Error

def reset_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='social_media'
        )
        cursor = connection.cursor()
        # Truncate tables to clear existing data
        tables = ['login', 'comment_likes', 'post_likes', 'comments', 'follows', 
                  'videos', 'photos', 'posts', 'users']
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
    except Error as e:
        print(f"Error resetting database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_sample_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='social_media'
        )
        cursor = connection.cursor()

        # Reset database to avoid duplicate errors
        reset_database()

        # Insert users
        users = [
            ('Ravi', 'ravi@gmail.com', 'https://picsum.photos/100', 'Studying at TCS'),
            ('Neha', 'neha@gmail.com', 'https://picsum.photos/101', 'Photographer and blogger'),
            ('Amit', 'amit@gmail.com', 'https://picsum.photos/102', 'Working at Infosys'),
            ('Tina', 'tina@gmail.com', 'https://picsum.photos/103', 'Engineering student'),
            ('Raj', 'raj@gmail.com', 'https://picsum.photos/104', 'Music lover and web dev'),
            ('Zara', 'zara@gmail.com', 'https://picsum.photos/105', 'Designing digital dreams'),
            ('Kabir', 'kabir@gmail.com', 'https://picsum.photos/106', 'Frontend intern'),
            ('Anya', 'anya@gmail.com', 'https://picsum.photos/107', 'Exploring tech & tea'),
            ('Mehul', 'mehul@gmail.com', 'https://picsum.photos/108', 'Freelancer & gamer'),
            ('Priya', 'priya@gmail.com', 'https://picsum.photos/109', 'Works at TCS'),
            ('Dev', 'dev@gmail.com', 'https://picsum.photos/110', 'Travel + tech'),
            ('Riya', 'riya@gmail.com', 'https://picsum.photos/111', 'Learning Oracle SQL'),
            ('Kunal', 'kunal@gmail.com', 'https://picsum.photos/112', 'Chai > Coffee'),
            ('Sneha', 'sneha@gmail.com', 'https://picsum.photos/113', 'Working @ Cognizant'),
            ('Arjun', 'arjun@gmail.com', 'https://picsum.photos/114', 'Fitness + coding'),
            ('Isha', 'isha@gmail.com', 'https://picsum.photos/115', 'Backend dev intern'),
            ('Rohit', 'rohit@gmail.com', 'https://picsum.photos/116', 'Studying CS @ MIT'),
            ('Kriti', 'kriti@gmail.com', 'https://picsum.photos/117', 'Writes code and poetry'),
            ('Nikhil', 'nikhil@gmail.com', 'https://picsum.photos/118', 'Passionate about AI'),
            ('Sana', 'sana@gmail.com', 'https://picsum.photos/119', 'Learning ReactJS')
        ]
        user_ids = {}
        for user in users:
            try:
                cursor.callproc('insert_user', user)
                cursor.execute("SELECT LAST_INSERT_ID()")
                user_id = cursor.fetchone()[0]
                user_ids[user[0]] = user_id
                print(f"Inserted user: {user[0]}, user_id: {user_id}")
                connection.commit()
            except Error as e:
                print(f"Failed to insert user {user[0]}: {e}")

        # Insert posts
        posts = [
            (1, 'HEY', 'Coimbatore'),
            (2, 'Live a good story.', 'The Red Fort, Delhi.'),
            (3, 'Escape the ordinary.', 'The Taj Mahal, Agra.'),
            (4, 'The best is yet to come.', 'Pangong Lake, Ladakh.'),
            (5, 'These are days we live for.', 'Valley of Flowers, Nainital.'),
            (6, 'Life happens, coffee helps.', 'Jaisalmer Fort, Jaisalmer.'),
            (7, 'Short sassy cute classy.', 'Ruins of Hampi, Karnataka.'),
            (8, 'The future is bright.', 'Agra'),
            (9, 'Namastay in bed.', 'Backwaters, Kerala.'),
            (10, 'I have more issues than vogue.', 'abhayapuri'),
            (1, 'Life is short. Smile while you still have teeth.', 'achabbal'),
            (12, 'Ah, a perfectly captured selfie!', 'achalpur'),
            (13, 'Let us just be who we are.', 'achhnera'),
            (14, 'One bad chapter doesn’t me', 'adari'),
            (5, 'Cinderella never asked for a prince.', 'Delhi'),
            (16, 'A selfie is worth a thousand words.', 'adilabad'),
            (17, 'Born to stand out with selfies.', 'adityana'),
            (18, 'I am sorry I exist, here, a selfie.', 'pereyaapatna'),
            (19, 'Ellipsis post', 'adoni'),  # Changed from '….'
            (2, 'depression', 'adoor')
        ]
        post_ids = {}
        for idx, post in enumerate(posts, 1):
            try:
                cursor.callproc('insert_post', post)
                cursor.execute("SELECT LAST_INSERT_ID()")
                post_id = cursor.fetchone()[0]
                post_ids[idx] = post_id
                print(f"Inserted post for user_id: {post[0]}, post_id: {post_id}")
                connection.commit()
            except Error as e:
                print(f"Failed to insert post for user_id {post[0]}: {e}")

        # Insert photos
        photos = [
            (1, 'https://picsum.photos/id/100/200', 4),
            (2, 'https://picsum.photos/id/101/200', 1),
            (3, 'https://picsum.photos/id/102/200', 2),
            (4, 'https://picsum.photos/id/103/200', 1),
            (5, 'https://picsum.photos/id/104/200', 2),
            (6, 'https://picsum.photos/id/105/200', 3),
            (7, 'https://picsum.photos/id/106/200', 4),
            (8, 'https://picsum.photos/id/107/200', 4),
            (9, 'https://picsum.photos/id/108/200', 2),
            (10, 'https://picsum.photos/id/109/200', 2),
            (11, 'https://picsum.photos/id/110/200', 2),
            (12, 'https://picsum.photos/id/111/200', 2),
            (13, 'https://picsum.photos/id/112/200', 2),
            (14, 'https://picsum.photos/id/113/200', 2),
            (15, 'https://picsum.photos/id/114/200', 4),
            (16, 'https://picsum.photos/id/115/200', 4),
            (17, 'https://picsum.photos/id/116/200', 3),
            (18, 'https://picsum.photos/id/117/200', 3),
            (19, 'https://picsum.photos/id/118/200', 3),
            (20, 'https://picsum.photos/id/119/200', 1)
        ]
        for photo in photos:
            try:
                cursor.callproc('insert_photo', photo)
                connection.commit()
            except Error as e:
                print(f"Error inserting photo for post_id {photo[0]}: {e}")

        # Insert videos
        videos = [
            (1, 'https://www.youtube.com/watch?v=1TKJvWbZErY', 1),
            (2, 'https://www.youtube.com/watch?v=dcgeBa78WE8', 8),
            (3, 'https://www.youtube.com/watch?v=vOfgVs6blGU', 3),
            (4, 'https://www.youtube.com/watch?v=gDGbwhoWRBQ', 2),
            (5, 'https://www.youtube.com/watch?v=UAj7FB-BFGg', 1),
            (6, 'https://www.youtube.com/watch?v=RzppsLjuSaI', 3),
            (7, 'https://www.youtube.com/watch?v=E1GLuxJ9mkU', 3),
            (8, 'https://www.youtube.com/watch?v=tjrFQQjTI6c', 2),
            (9, 'https://www.youtube.com/watch?v=IwNSd7m2HRg', 7),
            (10, 'https://www.youtube.com/watch?v=4javFbk9Kn8', 9),
            (11, 'https://www.youtube.com/watch?v=BuX7TQc4a0E', 4),
            (12, 'https://www.youtube.com/watch?v=4xx0YqaFalo', 7),
            (13, 'https://www.youtube.com/watch?v=n3LCQiuQn9o', 2),
            (14, 'https://www.youtube.com/watch?v=x9bmo0aPd0s', 1),
            (15, 'https://www.youtube.com/watch?v=UkTWeGJewTQ', 1),
            (16, 'https://www.youtube.com/watch?v=6GwUPaJh2Jg', 9),
            (17, 'https://www.youtube.com/watch?v=odHuMbTWIvU', 4),
            (18, 'https://www.youtube.com/watch?v=XxvEchaofrs', 8),
            (19, 'https://www.youtube.com/watch?v=3ZvSg5aU23E', 6),
            (20, 'https://www.youtube.com/watch?v=yBJM2RbLefA', 5)
        ]
        for video in videos:
            try:
                cursor.callproc('insert_video', video)
                connection.commit()
            except Error as e:
                print(f"Error inserting video for post_id {video[0]}: {e}")

        # Insert follows
        follows = [
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 1),
            (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 11)
        ]
        for follow in follows:
            try:
                cursor.callproc('insert_follow', follow)
                connection.commit()
            except Error as e:
                print(f"Error inserting follow for follower_id {follow[0]}: {e}")

        # Insert comments
        comments = [
            (1, 6, 'great man'),
            (12, 17, 'looking great bro'),
            (5, 15, 'nice place, keep enjoying'),
            (10, 11, 'awesome bro, meet you soon'),
            (7, 13, 'you set it on fire bro'),
            (3, 14, 'brilliant, keep working'),
            (9, 16, 'will join you all soon'),
            (18, 2, 'nice man!! loved it'),
            (19, 3, 'now the real deal will arrive'),
            (11, 4, 'you are getting too fast!'),
            (14, 5, 'you are really good, kid'),
            (17, 7, 'put it down, or else...'),
            (5, 10, 'how are you bro'),
            (6, 4, 'you set fire, we will need a fire extinguisher'),
            (8, 9, 'there is a story everyone should hear, it will burn even souls of the ignorant'),
            (20, 1, 'cool bro, meet me then I will show you who is really cool'),
            (13, 8, 'looking just right'),
            (16, 12, 'I think this is the best I have seen till now.'),
            (2, 13, 'Not enough for me, you are everything.'),
            (4, 6, 'Just when I could not love you more. You posted this pic and my jaw dropped to the floor.')
        ]
        for comment in comments:
            try:
                cursor.callproc('insert_comment', comment)
                connection.commit()
            except Error as e:
                print(f"Error inserting comment for post_id {comment[0]}: {e}")

        # Insert post_likes
        post_likes = [
            (1, 11), (2, 3), (3, 5), (4, 7), (5, 8), (6, 2), (7, 9), (8, 4), (9, 1), (10, 6),
            (11, 10), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)
        ]
        for like in post_likes:
            try:
                cursor.callproc('insert_post_like', like)
                connection.commit()
            except Error as e:
                print(f"Error inserting post_like for user_id {like[0]}: {e}")

        # Insert comment_likes
        comment_likes = [
            (1, 2), (3, 4), (4, 1), (3, 7), (8, 3), (6, 1), (5, 2), (6, 9), (2, 8), (9, 3),
            (7, 5), (10, 6), (11, 12), (12, 2), (13, 1), (14, 7), (15, 11), (16, 10), (17, 13), (18, 16)
        ]
        for like in comment_likes:
            try:
                cursor.callproc('insert_comment_like', like)
                connection.commit()
            except Error as e:
                print(f"Error inserting comment_like for user_id {like[0]}: {e}")

        # Insert login
        logins = [
            (19, '186.83.147.14'), (3, '95.43.246.66'), (7, '105.238.37.204'), (6, '13.120.97.136'),
            (6, '0.83.214.172'), (7, '20.182.93.222'), (11, '200.237.53.32'), (8, '41.81.231.81'),
            (9, '24.223.2.33'), (10, '8.168.37.68'), (12, '129.91.145.75'), (13, '8.65.175.204'),
            (15, '242.220.82.190'), (6, '107.137.170.154'), (10, '206.40.219.225'), (2, '136.186.80.29'),
            (13, '234.153.100.73'), (14, '137.168.133.16'), (18, '248.119.108.48'), (16, '92.178.211.66'),
            (17, '25.177.94.84')
        ]
        for login in logins:
            try:
                cursor.callproc('insert_login', login)
                connection.commit()
            except Error as e:
                print(f"Error inserting login for user_id {login[0]}: {e}")

        print("Sample data inserted successfully.")
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_sample_data()