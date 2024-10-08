import sqlite3


class TransactionManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_transaction(self, user_id, account_id, category_id, amount, transaction_type, description, date):
        try:
            self.cursor.execute("""
            INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, account_id, category_id, amount, transaction_type, description, date))
            self.cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm giao dịch: {e}")

    def get_all_transactions(self, user_id):
        self.cursor.execute("""
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()

    def get_transactions_from_start_of_october(self, user_id):
        self.cursor.execute("""
        SELECT * FROM transactions 
        WHERE user_id = ? AND created_at >= '2024-10-01' 
        ORDER BY created_at DESC;
        """, (user_id,))
        return self.cursor.fetchall()

    def get_category_statistics_from_start_of_october(self, user_id):
        self.cursor.execute("""
        SELECT categories.category_name, SUM(transactions.amount) as total_amount
        FROM transactions 
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.created_at >= '2024-10-01'
        GROUP BY categories.category_name
        ORDER BY total_amount DESC;
        """, (user_id,))
        return self.cursor.fetchall()
