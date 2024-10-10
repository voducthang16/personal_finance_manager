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

    def get_transactions_by_date_range(self, user_id, start_date, end_date):
        """Lấy giao dịch từ khoảng thời gian nhất định."""
        self.cursor.execute("""
        SELECT * FROM transactions 
        WHERE user_id = ? AND date BETWEEN ? AND ?
        ORDER BY date DESC;
        """, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def get_category_statistics_by_date_range(self, user_id, start_date, end_date):
        """Lấy thống kê danh mục giao dịch từ khoảng thời gian nhất định."""
        self.cursor.execute("""
        SELECT categories.category_name, SUM(transactions.amount) as total_amount
        FROM transactions 
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.date BETWEEN ? AND ?
        GROUP BY categories.category_name
        ORDER BY total_amount DESC;
        """, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def get_total_income(self, user_id, start_date, end_date):
        """Lấy tổng thu nhập trong khoảng thời gian."""
        self.cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND transaction_type = 'Thu nhập' AND date BETWEEN ? AND ?
        """, (user_id, start_date, end_date))
        return self.cursor.fetchone()[0] or 0  # Nếu không có dữ liệu, trả về 0

    def get_total_expense(self, user_id, start_date, end_date):
        """Lấy tổng chi tiêu trong khoảng thời gian."""
        self.cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND transaction_type = 'Chi tiêu' AND date BETWEEN ? AND ?
        """, (user_id, start_date, end_date))
        return self.cursor.fetchone()[0] or 0

    def get_total_balance(self, user_id):
        """Lấy tổng số dư hiện tại từ tất cả các tài khoản."""
        self.cursor.execute("""
        SELECT SUM(balance) FROM accounts 
        WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchone()[0] or 0