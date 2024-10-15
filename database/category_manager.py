import sqlite3
from utils import tuples_to_dicts


class CategoryManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_category(self, category_name, category_type):
        try:
            self.cursor.execute("""
            INSERT INTO categories (category_name, category_type, created_at, updated_at, is_deleted)
            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """, (category_name, category_type))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm danh mục: {e}")

    def update_category(self, category_id, category_name, category_type):
        try:
            self.cursor.execute("""
                UPDATE categories
                SET category_name = ?, category_type = ?, updated_at = CURRENT_TIMESTAMP
                WHERE category_id = ? AND is_deleted = 0
            """, (category_name, category_type, category_id))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật danh mục: {e}")

    def delete_category(self, category_id):
        try:
            self.cursor.execute("""
                UPDATE categories
                SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
                WHERE category_id = ?
            """, (category_id,))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa danh mục: {e}")
            raise e

    def get_categories(self, limit, offset):
        self.cursor.execute("""
        SELECT * FROM categories 
        WHERE is_deleted = 0
        ORDER BY categories.category_id DESC
        LIMIT ? OFFSET ?
        """, (limit, offset))

        columns = [column[0] for column in self.cursor.description]
        categories_tuples = self.cursor.fetchall()

        return tuples_to_dicts(categories_tuples, columns)

    def count_categories(self):
        self.cursor.execute("""
        SELECT COUNT(*) FROM categories WHERE is_deleted = 0
        """)
        return self.cursor.fetchone()[0]
