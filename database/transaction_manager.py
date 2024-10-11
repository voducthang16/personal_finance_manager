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

    def get_all_transactions(self, user_id, limit=None, offset=None):
        """Lấy tất cả các giao dịch của người dùng, hỗ trợ phân trang với limit và offset."""
        query = """
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ?
        """

        params = [user_id]
        if limit is not None and offset is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return self.convert_to_dicts(results, self.get_transaction_columns())

    def get_transaction_columns(self):
        """Lấy các tên cột của bảng giao dịch để tiện cho việc chuyển đổi kết quả."""
        return ["transaction_id", "user_id", "account_id", "category_id", "amount", "transaction_type",
                "description", "date", "created_at", "account_name", "category_name"]

    def get_transactions_by_date_range(self, user_id, start_date, end_date, limit=None, offset=None):
        """Lấy giao dịch từ khoảng thời gian nhất định, hỗ trợ phân trang."""
        query = """
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.date BETWEEN ? AND ?
        ORDER BY date DESC
        """

        params = [user_id, start_date, end_date]
        if limit is not None and offset is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return self.convert_to_dicts(results, self.get_transaction_columns())

    def convert_to_dicts(self, rows, columns):
        """Chuyển danh sách tuple thành danh sách dictionary dựa trên tên cột."""
        return [dict(zip(columns, row)) for row in rows]

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
