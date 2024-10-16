import sqlite3
from utils import tuples_to_dicts


class AccountManager:
    def __init__(self, cursor, user_manager):
        self.cursor = cursor
        self.user_manager = user_manager

    def is_account_name_exists(self, user_id, account_name, account_id=None):
        try:
            if account_id:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM accounts
                    WHERE user_id = ? AND account_name = ? AND account_id != ? AND is_deleted = 0
                """, (user_id, account_name, account_id))
            else:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM accounts
                    WHERE user_id = ? AND account_name = ? AND is_deleted = 0
                """, (user_id, account_name))
            result = self.cursor.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print(f"Lỗi khi kiểm tra tên tài khoản: {e}")
            return False

    def add_account(self, user_id, account_name, balance=0):
        if self.is_account_name_exists(user_id, account_name):
            return f"Lỗi: Tài khoản '{account_name}' đã tồn tại."

        if balance <= 0:
            return "Số dư phải lớn hơn 0."

        try:
            self.cursor.execute("""
                INSERT INTO accounts (user_id, account_name, balance, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """, (user_id, account_name, balance))
            self.cursor.connection.commit()
            return None  # Thành công
        except sqlite3.Error as e:
            return f"Lỗi khi thêm tài khoản: {e}"

    def update_account(self, account_id, account_name, balance):
        user = self.user_manager.get_first_user()

        user_id = user["user_id"]

        if self.is_account_name_exists(user_id, account_name, account_id):
            return f"Lỗi: Tài khoản '{account_name}' đã tồn tại."

        if balance <= 0:
            return "Số dư phải lớn hơn 0."

        try:
            self.cursor.execute("""
                UPDATE accounts
                SET account_name = ?, balance = ?, updated_at = CURRENT_TIMESTAMP
                WHERE account_id = ? AND is_deleted = 0
            """, (account_name, balance, account_id))
            self.cursor.connection.commit()
            return None
        except sqlite3.Error as e:
            return f"Lỗi khi cập nhật tài khoản: {e}"

    def delete_account(self, account_id):
        try:
            self.cursor.execute("""
                UPDATE accounts
                SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
                WHERE account_id = ?
            """, (account_id,))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa tài khoản: {e}")
            raise e

    def get_accounts_for_user(self, user_id, limit, offset):
        self.cursor.execute("""
        SELECT * FROM accounts 
        WHERE user_id = ? AND is_deleted = 0
        ORDER BY accounts.account_id DESC
        LIMIT ? OFFSET ?
        """, (user_id, limit, offset))

        columns = [column[0] for column in self.cursor.description]
        accounts_tuples = self.cursor.fetchall()

        return tuples_to_dicts(accounts_tuples, columns)

    def count_accounts_for_user(self, user_id):
        self.cursor.execute("""
        SELECT COUNT(*) FROM accounts 
        WHERE user_id = ? AND is_deleted = 0
        """, (user_id,))
        return self.cursor.fetchone()[0]
