import sqlite3
from utils import tuples_to_dicts


class AccountManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_account(self, user_id, account_name, balance=0):
        try:
            self.cursor.execute("""
            INSERT INTO accounts (user_id, account_name, balance, created_at, updated_at, is_deleted)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """, (user_id, account_name, balance))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm tài khoản: {e}")

    def update_account(self, account_id, account_name, balance):
        try:
            self.cursor.execute("""
                UPDATE accounts
                SET account_name = ?, balance = ?, updated_at = CURRENT_TIMESTAMP
                WHERE account_id = ? AND is_deleted = 0
            """, (account_name, balance, account_id))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật tài khoản: {e}")

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
        LIMIT ? OFFSET ?
        """, (user_id, limit, offset))

        columns = [column[0] for column in self.cursor.description]
        accounts_tuples = self.cursor.fetchall()

        # Convert tuples to dicts using the utility function
        return tuples_to_dicts(accounts_tuples, columns)

    def count_accounts_for_user(self, user_id):
        self.cursor.execute("""
        SELECT COUNT(*) FROM accounts 
        WHERE user_id = ? AND is_deleted = 0
        """, (user_id,))
        return self.cursor.fetchone()[0]
