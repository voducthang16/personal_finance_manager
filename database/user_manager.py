import sqlite3

from utils import tuples_to_dicts


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
            SET name = ?, email = ?, updated_at = CURRENT_TIMESTAMP
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
            columns = [description[0] for description in self.cursor.description]
            user_dict = tuples_to_dicts([row], columns)[0]  # Vì chỉ có 1 kết quả nên lấy phần tử đầu tiên
            return user_dict
        return None
