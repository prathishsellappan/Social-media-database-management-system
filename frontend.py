import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import re

class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Database Management")
        self.root.geometry("800x600")

        self.conn = None
        self.cursor = None
        self.connect_db()

        self.create_widgets()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='social_media'
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            self.root.quit()

    def create_widgets(self):
        # Menu frame
        menu_frame = ttk.LabelFrame(self.root, text="Menu Options")
        menu_frame.pack(padx=10, pady=10, fill="x")

        options = [
            "Insert User", "Insert Post", "Insert Photo", "Insert Video", "Insert Follow",
            "Insert Comment", "Insert Post Like", "Insert Comment Like", "Insert Login",
            "Delete User", "Delete Post", "Delete Photo", "Delete Video", "Delete Follow",
            "Delete Comment", "Delete Post Like", "Delete Comment Like", "Delete Login",
            "Get Most Inactive Users", "Get Most Liked Posts", "Get Average Posts per User",
            "Get Login Count per User", "Get Users Who Never Commented", "Get Users Not Followed",
            "Get Users Not Following", "Get Longest Captions", "Get Top Posters"
        ]

        self.choice_var = tk.StringVar()
        ttk.Combobox(menu_frame, textvariable=self.choice_var, values=options, state="readonly").pack(pady=5)
        ttk.Button(menu_frame, text="Execute", command=self.execute_choice).pack(pady=5)

        # Output area
        self.output_text = scrolledtext.ScrolledText(self.root, height=20, width=80)
        self.output_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Exit button
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def validate_email(self, email):
        """Validate email format."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def validate_ip(self, ip):
        """Validate IP address format."""
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        return bool(re.match(pattern, ip)) and all(0 <= int(part) <= 255 for part in ip.split('.'))

    def check_unique_username(self, username):
        """Check if username is unique."""
        self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        return self.cursor.fetchone() is None

    def check_unique_email(self, email):
        """Check if email is unique."""
        self.cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        return self.cursor.fetchone() is None

    def check_user_exists(self, user_id):
        """Check if user_id exists."""
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone() is not None

    def check_post_exists(self, post_id):
        """Check if post_id exists."""
        self.cursor.execute("SELECT post_id FROM posts WHERE post_id = %s", (post_id,))
        return self.cursor.fetchone() is not None

    def check_photo_exists(self, photo_id):
        """Check if photo_id exists."""
        self.cursor.execute("SELECT photo_id FROM photos WHERE photo_id = %s", (photo_id,))
        return self.cursor.fetchone() is not None

    def check_video_exists(self, video_id):
        """Check if video_id exists."""
        self.cursor.execute("SELECT video_id FROM videos WHERE video_id = %s", (video_id,))
        return self.cursor.fetchone() is not None

    def check_follow_exists(self, follower_id, followee_id):
        """Check if follow relationship exists."""
        self.cursor.execute("SELECT follower_id, followee_id FROM follows WHERE follower_id = %s AND followee_id = %s", (follower_id, followee_id))
        return self.cursor.fetchone() is not None

    def check_comment_exists(self, comment_id):
        """Check if comment_id exists."""
        self.cursor.execute("SELECT comment_id FROM comments WHERE comment_id = %s", (comment_id,))
        return self.cursor.fetchone() is not None

    def check_post_like_exists(self, user_id, post_id):
        """Check if post_like pair exists."""
        self.cursor.execute("SELECT user_id, post_id FROM post_likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        return self.cursor.fetchone() is not None

    def check_comment_like_exists(self, user_id, comment_id):
        """Check if comment_like pair exists."""
        self.cursor.execute("SELECT user_id, comment_id FROM comment_likes WHERE user_id = %s AND comment_id = %s", (user_id, comment_id))
        return self.cursor.fetchone() is not None

    def check_login_exists(self, login_id):
        """Check if login_id exists."""
        self.cursor.execute("SELECT login_id FROM login WHERE login_id = %s", (login_id,))
        return self.cursor.fetchone() is not None

    def check_post_like_unique(self, user_id, post_id):
        """Check if post_like pair is unique."""
        self.cursor.execute("SELECT user_id, post_id FROM post_likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
        return self.cursor.fetchone() is None

    def check_comment_like_unique(self, user_id, comment_id):
        """Check if comment_like pair is unique."""
        self.cursor.execute("SELECT user_id, comment_id FROM comment_likes WHERE user_id = %s AND comment_id = %s", (user_id, comment_id))
        return self.cursor.fetchone() is None

    def execute_choice(self):
        choice = self.choice_var.get()
        self.output_text.delete(1.0, tk.END)

        try:
            if choice == "Insert User":
                username = simpledialog.askstring("Input", "Enter username:", parent=self.root)
                if not username or len(username.strip()) == 0:
                    self.output_text.insert(tk.END, "Error: Username cannot be empty.\n")
                    return
                if not self.check_unique_username(username):
                    self.output_text.insert(tk.END, "Error: Username already exists.\n")
                    return

                email = simpledialog.askstring("Input", "Enter email:", parent=self.root)
                if not email or not self.validate_email(email):
                    self.output_text.insert(tk.END, "Error: Invalid or empty email.\n")
                    return
                if not self.check_unique_email(email):
                    self.output_text.insert(tk.END, "Error: Email already exists.\n")
                    return

                bio = simpledialog.askstring("Input", "Enter bio (optional):", parent=self.root)
                if bio is None:  # User clicked Cancel
                    return
                bio = bio.strip() if bio else ""

                photo_url = simpledialog.askstring("Input", "Enter profile photo URL (optional, press OK for default):", parent=self.root)
                if photo_url is None:  # User clicked Cancel
                    return
                photo_url = photo_url.strip() if photo_url else "https://picsum.photos/200"

                self.cursor.callproc('insert_user', (username, email, photo_url, bio))
                self.conn.commit()
                self.output_text.insert(tk.END, f"User '{username}' inserted successfully.\n")

            elif choice == "Insert Post":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                caption = simpledialog.askstring("Input", "Enter caption:", parent=self.root)
                if not caption or len(caption.strip()) == 0:
                    self.output_text.insert(tk.END, "Error: Caption cannot be empty.\n")
                    return
                if len(caption) > 500:
                    self.output_text.insert(tk.END, "Error: Caption exceeds 500 characters.\n")
                    return

                location = simpledialog.askstring("Input", "Enter location (optional):", parent=self.root)
                if location is None:  # User clicked Cancel
                    return
                location = location.strip() if location else ""

                self.cursor.callproc('insert_post', (user_id, caption, location))
                self.conn.commit()
                self.output_text.insert(tk.END, "Post inserted successfully.\n")

            elif choice == "Insert Photo":
                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                photo_url = simpledialog.askstring("Input", "Enter photo URL:", parent=self.root)
                if not photo_url or len(photo_url.strip()) == 0:
                    self.output_text.insert(tk.END, "Error: Photo URL cannot be empty.\n")
                    return

                photo_size = simpledialog.askstring("Input", "Enter photo size (MB, < 5):", parent=self.root)
                if not photo_size or not photo_size.isdigit():
                    self.output_text.insert(tk.END, "Error: Photo size must be a number.\n")
                    return
                photo_size = int(photo_size)
                if photo_size >= 5:
                    self.output_text.insert(tk.END, "Error: Photo size must be less than 5 MB.\n")
                    return

                self.cursor.callproc('insert_photo', (post_id, photo_url, photo_size))
                self.conn.commit()
                self.output_text.insert(tk.END, "Photo inserted successfully.\n")

            elif choice == "Insert Video":
                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                video_url = simpledialog.askstring("Input", "Enter video URL:", parent=self.root)
                if not video_url or len(video_url.strip()) == 0:
                    self.output_text.insert(tk.END, "Error: Video URL cannot be empty.\n")
                    return

                video_size = simpledialog.askstring("Input", "Enter video size (MB, < 10):", parent=self.root)
                if not video_size or not video_size.isdigit():
                    self.output_text.insert(tk.END, "Error: Video size must be a number.\n")
                    return
                video_size = int(video_size)
                if video_size >= 10:
                    self.output_text.insert(tk.END, "Error: Video size must be less than 10 MB.\n")
                    return

                self.cursor.callproc('insert_video', (post_id, video_url, video_size))
                self.conn.commit()
                self.output_text.insert(tk.END, "Video inserted successfully.\n")

            elif choice == "Insert Follow":
                follower_id = simpledialog.askstring("Input", "Enter follower ID:", parent=self.root)
                if not follower_id or not follower_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Follower ID must be a number.\n")
                    return
                follower_id = int(follower_id)
                if not self.check_user_exists(follower_id):
                    self.output_text.insert(tk.END, "Error: Follower ID does not exist.\n")
                    return

                followee_id = simpledialog.askstring("Input", "Enter followee ID:", parent=self.root)
                if not followee_id or not followee_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Followee ID must be a number.\n")
                    return
                followee_id = int(followee_id)
                if not self.check_user_exists(followee_id):
                    self.output_text.insert(tk.END, "Error: Followee ID does not exist.\n")
                    return

                if follower_id == followee_id:
                    self.output_text.insert(tk.END, "Error: User cannot follow themselves.\n")
                    return

                self.cursor.callproc('insert_follow', (follower_id, followee_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Follow inserted successfully.\n")

            elif choice == "Insert Comment":
                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                content = simpledialog.askstring("Input", "Enter comment content:", parent=self.root)
                if not content or len(content.strip()) == 0:
                    self.output_text.insert(tk.END, "Error: Comment content cannot be empty.\n")
                    return
                if len(content) > 500:
                    self.output_text.insert(tk.END, "Error: Comment exceeds 500 characters.\n")
                    return

                self.cursor.callproc('insert_comment', (post_id, user_id, content))
                self.conn.commit()
                self.output_text.insert(tk.END, "Comment inserted successfully.\n")

            elif choice == "Insert Post Like":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                if not self.check_post_like_unique(user_id, post_id):
                    self.output_text.insert(tk.END, "Error: User has already liked this post.\n")
                    return

                self.cursor.callproc('insert_post_like', (user_id, post_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Post like inserted successfully.\n")

            elif choice == "Insert Comment Like":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                comment_id = simpledialog.askstring("Input", "Enter comment ID:", parent=self.root)
                if not comment_id or not comment_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Comment ID must be a number.\n")
                    return
                comment_id = int(comment_id)
                if not self.check_comment_exists(comment_id):
                    self.output_text.insert(tk.END, "Error: Comment ID does not exist.\n")
                    return

                if not self.check_comment_like_unique(user_id, comment_id):
                    self.output_text.insert(tk.END, "Error: User has already liked this comment.\n")
                    return

                self.cursor.callproc('insert_comment_like', (user_id, comment_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Comment like inserted successfully.\n")

            elif choice == "Insert Login":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                ip = simpledialog.askstring("Input", "Enter IP address:", parent=self.root)
                if not ip or not self.validate_ip(ip):
                    self.output_text.insert(tk.END, "Error: Invalid or empty IP address.\n")
                    return

                self.cursor.callproc('insert_login', (user_id, ip))
                self.conn.commit()
                self.output_text.insert(tk.END, "Login inserted successfully.\n")

            elif choice == "Delete User":
                messagebox.showwarning(
                    "Warning",
                    "Deleting a user will also delete all their posts, comments, follows, likes, and login records.",
                    parent=self.root
                )
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                self.cursor.callproc('delete_user', (user_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "User and all associated records deleted successfully.\n")

            elif choice == "Delete Post":
                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                self.cursor.callproc('delete_post', (post_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "Post and all associated records deleted successfully.\n")

            elif choice == "Delete Photo":
                photo_id = simpledialog.askstring("Input", "Enter photo ID:", parent=self.root)
                if not photo_id or not photo_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Photo ID must be a number.\n")
                    return
                photo_id = int(photo_id)
                if not self.check_photo_exists(photo_id):
                    self.output_text.insert(tk.END, "Error: Photo ID does not exist.\n")
                    return

                self.cursor.callproc('delete_photo', (photo_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "Photo deleted successfully.\n")

            elif choice == "Delete Video":
                video_id = simpledialog.askstring("Input", "Enter video ID:", parent=self.root)
                if not video_id or not video_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Video ID must be a number.\n")
                    return
                video_id = int(video_id)
                if not self.check_video_exists(video_id):
                    self.output_text.insert(tk.END, "Error: Video ID does not exist.\n")
                    return

                self.cursor.callproc('delete_video', (video_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "Video deleted successfully.\n")

            elif choice == "Delete Follow":
                follower_id = simpledialog.askstring("Input", "Enter follower ID:", parent=self.root)
                if not follower_id or not follower_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Follower ID must be a number.\n")
                    return
                follower_id = int(follower_id)
                if not self.check_user_exists(follower_id):
                    self.output_text.insert(tk.END, "Error: Follower ID does not exist.\n")
                    return

                followee_id = simpledialog.askstring("Input", "Enter followee ID:", parent=self.root)
                if not followee_id or not followee_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Followee ID must be a number.\n")
                    return
                followee_id = int(followee_id)
                if not self.check_user_exists(followee_id):
                    self.output_text.insert(tk.END, "Error: Followee ID does not exist.\n")
                    return

                if not self.check_follow_exists(follower_id, followee_id):
                    self.output_text.insert(tk.END, "Error: Follow relationship does not exist.\n")
                    return

                self.cursor.callproc('delete_follow', (follower_id, followee_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Follow deleted successfully.\n")

            elif choice == "Delete Comment":
                comment_id = simpledialog.askstring("Input", "Enter comment ID:", parent=self.root)
                if not comment_id or not comment_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Comment ID must be a number.\n")
                    return
                comment_id = int(comment_id)
                if not self.check_comment_exists(comment_id):
                    self.output_text.insert(tk.END, "Error: Comment ID does not exist.\n")
                    return

                self.cursor.callproc('delete_comment', (comment_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "Comment and all associated likes deleted successfully.\n")

            elif choice == "Delete Post Like":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                post_id = simpledialog.askstring("Input", "Enter post ID:", parent=self.root)
                if not post_id or not post_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Post ID must be a number.\n")
                    return
                post_id = int(post_id)
                if not self.check_post_exists(post_id):
                    self.output_text.insert(tk.END, "Error: Post ID does not exist.\n")
                    return

                if not self.check_post_like_exists(user_id, post_id):
                    self.output_text.insert(tk.END, "Error: Post like does not exist.\n")
                    return

                self.cursor.callproc('delete_post_like', (user_id, post_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Post like deleted successfully.\n")

            elif choice == "Delete Comment Like":
                user_id = simpledialog.askstring("Input", "Enter user ID:", parent=self.root)
                if not user_id or not user_id.isdigit():
                    self.output_text.insert(tk.END, "Error: User ID must be a number.\n")
                    return
                user_id = int(user_id)
                if not self.check_user_exists(user_id):
                    self.output_text.insert(tk.END, "Error: User ID does not exist.\n")
                    return

                comment_id = simpledialog.askstring("Input", "Enter comment ID:", parent=self.root)
                if not comment_id or not comment_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Comment ID must be a number.\n")
                    return
                comment_id = int(comment_id)
                if not self.check_comment_exists(comment_id):
                    self.output_text.insert(tk.END, "Error: Comment ID does not exist.\n")
                    return

                if not self.check_comment_like_exists(user_id, comment_id):
                    self.output_text.insert(tk.END, "Error: Comment like does not exist.\n")
                    return

                self.cursor.callproc('delete_comment_like', (user_id, comment_id))
                self.conn.commit()
                self.output_text.insert(tk.END, "Comment like deleted successfully.\n")

            elif choice == "Delete Login":
                login_id = simpledialog.askstring("Input", "Enter login ID:", parent=self.root)
                if not login_id or not login_id.isdigit():
                    self.output_text.insert(tk.END, "Error: Login ID must be a number.\n")
                    return
                login_id = int(login_id)
                if not self.check_login_exists(login_id):
                    self.output_text.insert(tk.END, "Error: Login ID does not exist.\n")
                    return

                self.cursor.callproc('delete_login', (login_id,))
                self.conn.commit()
                self.output_text.insert(tk.END, "Login deleted successfully.\n")

            elif choice == "Get Most Inactive Users":
                self.cursor.callproc('get_most_inactive_users')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}\n")

            elif choice == "Get Most Liked Posts":
                self.cursor.callproc('get_most_liked_posts')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"Post ID: {row[0]}, Likes: {row[1]}\n")

            elif choice == "Get Average Posts per User":
                self.cursor.callproc('get_avg_posts_per_user')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"Average Posts per User: {row[0]}\n")

            elif choice == "Get Login Count per User":
                self.cursor.callproc('get_login_count_per_user')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}, Logins: {row[2]}\n")

            elif choice == "Get Users Who Never Commented":
                self.cursor.callproc('get_users_never_commented')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}\n")

            elif choice == "Get Users Not Followed":
                self.cursor.callproc('get_users_not_followed')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}\n")

            elif choice == "Get Users Not Following":
                self.cursor.callproc('get_users_not_following')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}\n")

            elif choice == "Get Longest Captions":
                self.cursor.callproc('get_longest_captions')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Caption Length: {row[2]}, Caption: {row[1]}\n")

            elif choice == "Get Top Posters":
                self.cursor.callproc('get_top_posters')
                for result in self.cursor.stored_results():
                    for row in result.fetchall():
                        self.output_text.insert(tk.END, f"User ID: {row[0]}, Username: {row[1]}, Total Posts: {row[2]}\n")

            else:
                self.output_text.insert(tk.END, "Please select a valid option.\n")

        except Error as e:
            self.output_text.insert(tk.END, f"Error executing procedure: {e}\n")

    def __del__(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaApp(root)
    root.mainloop()