import sqlite3


class AccountManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_account(self, user_id, account_name, balance=0):
        try:
            self.cursor.execute("""
            INSERT INTO accounts (user_id, account_name, balance)
            VALUES (?, ?, ?)
            """, (user_id, account_name, balance))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm tài khoản: {e}")

    def update_account(self, account_id, account_name, balance):
        try:
            self.cursor.execute("""
                UPDATE accounts
                SET account_name = ?, balance = ?
                WHERE account_id = ?
            """, (account_name, balance, account_id))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating account: {e}")

    def delete_account(self, account_id):
        try:
            self.cursor.execute("""
                DELETE FROM accounts 
                WHERE account_id = ?
            """, (account_id,))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa tài khoản: {e}")
            raise e

    def get_accounts_for_user(self, user_id, limit, offset):
        """Lấy danh sách tài khoản của người dùng"""
        self.cursor.execute("""
        SELECT * FROM accounts WHERE user_id = ? LIMIT ? OFFSET ?
        """, (user_id, limit, offset))
        columns = [column[0] for column in self.cursor.description]
        accounts = []
        for row in self.cursor.fetchall():
            account_dict = dict(zip(columns, row))
            accounts.append(account_dict)
        return accounts

    def count_accounts_for_user(self, user_id):
        self.cursor.execute("""
        SELECT COUNT(*) FROM accounts WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchone()[0]
