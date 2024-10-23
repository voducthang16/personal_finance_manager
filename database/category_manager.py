import sqlite3
from utils import tuples_to_dicts


class CategoryManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def is_category_name_exists(self, category_name, category_id=None):
        try:
            if category_id:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM categories
                    WHERE category_name = ? AND category_id != ? AND is_deleted = 0
                """, (category_name, category_id))
            else:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM categories
                    WHERE category_name = ? AND is_deleted = 0
                """, (category_name,))
            result = self.cursor.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print(f"Lỗi khi kiểm tra tên danh mục: {e}")
            return False

    def add_category(self, category_name, category_type):
        if self.is_category_name_exists(category_name):
            return f"Lỗi: Danh mục '{category_name}' đã tồn tại."
        try:
            self.cursor.execute("""
                INSERT INTO categories (category_name, category_type, created_at, updated_at, is_deleted)
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """, (category_name, category_type))
            self.cursor.connection.commit()
            return None
        except sqlite3.Error as e:
            return f"Lỗi khi thêm danh mục: {e}"

    def update_category(self, category_id, category_name, category_type):
        if self.is_category_name_exists(category_name, category_id):
            return f"Lỗi: Danh mục '{category_name}' đã tồn tại."
        try:
            self.cursor.execute("""
                UPDATE categories
                SET category_name = ?, category_type = ?, updated_at = CURRENT_TIMESTAMP
                WHERE category_id = ? AND is_deleted = 0
            """, (category_name, category_type, category_id))
            self.cursor.connection.commit()
            return None
        except sqlite3.Error as e:
            return f"Lỗi khi cập nhật danh mục: {e}"

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

    def get_category_id_by_name(self, category_name):
        try:
            self.cursor.execute("""
                SELECT category_id FROM categories
                WHERE category_name = ? AND is_deleted = 0
            """, (category_name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Lỗi khi lấy category_id từ category_name '{category_name}': {e}")
            return None

    def count_categories(self):
        self.cursor.execute("""
        SELECT COUNT(*) FROM categories WHERE is_deleted = 0
        """)
        return self.cursor.fetchone()[0]
