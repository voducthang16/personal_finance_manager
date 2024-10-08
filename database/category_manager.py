import sqlite3

from utils import tuples_to_dicts


class CategoryManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_category(self, category_name, category_type):
        try:
            self.cursor.execute("""
            INSERT INTO categories (category_name, category_type)
            VALUES (?, ?)
            """, (category_name, category_type))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm danh mục: {e}")

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")

        # Lấy tên cột
        columns = [column[0] for column in self.cursor.description]
        categories_tuples = self.cursor.fetchall()

        # Convert tuples to dicts using the utility function
        return tuples_to_dicts(categories_tuples, columns)
