import sqlite3


class UserManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_user(self, name, email):
        try:
            self.cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
            """, (name, email))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm người dùng: {e}")
            raise e

    def update_user(self, user_id, name, email):
        try:
            self.cursor.execute("""
            UPDATE users 
            SET name = ?, email = ?
            WHERE user_id = ?
            """, (name, email, user_id))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật người dùng: {e}")
            raise e

    def get_first_user(self):
        self.cursor.execute("SELECT * FROM users ORDER BY user_id ASC LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3]
            }
        return None
