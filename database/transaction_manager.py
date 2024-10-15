import sqlite3

from utils import tuples_to_dicts


class TransactionManager:
    def __init__(self, cursor):
        self.cursor = cursor

    def add_transaction(self, user_id, account_id, category_id, amount, transaction_type, description, date):
        try:
            # Bắt đầu transaction để đảm bảo tính toàn vẹn dữ liệu
            self.cursor.connection.execute("BEGIN TRANSACTION")

            # Thêm giao dịch vào bảng transactions
            self.cursor.execute("""
            INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date, created_at, updated_at, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            """, (user_id, account_id, category_id, amount, transaction_type, description, date))

            # Cập nhật số dư trong tài khoản
            if transaction_type == "Thu nhập":
                self.cursor.execute("""
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_id = ? AND user_id = ?
                """, (amount, account_id, user_id))
            elif transaction_type == "Chi tiêu":
                self.cursor.execute("""
                UPDATE accounts
                SET balance = balance - ?
                WHERE account_id = ? AND user_id = ?
                """, (amount, account_id, user_id))

            # Commit transaction nếu không có lỗi xảy ra
            self.cursor.connection.commit()

        except sqlite3.Error as e:
            # Rollback nếu có lỗi
            self.cursor.connection.rollback()
            print(f"Lỗi khi thêm giao dịch: {e}")

    def update_transaction(self, transaction_id, amount, transaction_type, description, date):
        try:
            # Bắt đầu transaction
            self.cursor.connection.execute("BEGIN TRANSACTION")

            self.cursor.execute("""
            SELECT account_id, amount, transaction_type FROM transactions
            WHERE transaction_id = ? AND is_deleted = 0
            """, (transaction_id,))
            old_transaction = self.cursor.fetchone()

            if old_transaction:
                old_account_id, old_amount, old_transaction_type = old_transaction

                # Hoàn tác thay đổi số dư của giao dịch cũ
                if old_transaction_type == "Thu nhập":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance - ?
                    WHERE account_id = ?
                    """, (old_amount, old_account_id))
                elif old_transaction_type == "Chi tiêu":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?
                    """, (old_amount, old_account_id))

                # Cập nhật giao dịch mới
                self.cursor.execute("""
                UPDATE transactions
                SET amount = ?, transaction_type = ?, description = ?, date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE transaction_id = ? AND is_deleted = 0
                """, (amount, transaction_type, description, date, transaction_id))

                # Cập nhật lại số dư cho giao dịch mới
                if transaction_type == "Thu nhập":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?
                    """, (amount, old_account_id))
                elif transaction_type == "Chi tiêu":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance - ?
                    WHERE account_id = ?
                    """, (amount, old_account_id))

                # Commit thay đổi
                self.cursor.connection.commit()
            else:
                print("Giao dịch không tồn tại hoặc đã bị xóa.")

        except sqlite3.Error as e:
            self.cursor.connection.rollback()
            print(f"Lỗi khi cập nhật giao dịch: {e}")

    def delete_transaction(self, transaction_id):
        try:
            self.cursor.connection.execute("BEGIN TRANSACTION")

            self.cursor.execute("""
            SELECT account_id, amount, transaction_type FROM transactions
            WHERE transaction_id = ? AND is_deleted = 0
            """, (transaction_id,))
            transaction = self.cursor.fetchone()

            if transaction:
                account_id, amount, transaction_type = transaction

                # Hoàn tác số dư dựa trên loại giao dịch
                if transaction_type == "Thu nhập":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance - ?
                    WHERE account_id = ?
                    """, (amount, account_id))
                elif transaction_type == "Chi tiêu":
                    self.cursor.execute("""
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_id = ?
                    """, (amount, account_id))

                # Đánh dấu giao dịch là đã xóa
                self.cursor.execute("""
                UPDATE transactions
                SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP
                WHERE transaction_id = ?
                """, (transaction_id,))

                # Commit transaction
                self.cursor.connection.commit()
            else:
                print("Giao dịch không tồn tại hoặc đã bị xóa.")

        except sqlite3.Error as e:
            self.cursor.connection.rollback()
            print(f"Lỗi khi xóa giao dịch: {e}")

    def get_all_transactions(self, user_id, limit=None, offset=None):
        query = """
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.is_deleted = 0
        ORDER BY transactions.transaction_id DESC
        """

        params = [user_id]
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)

        if offset is not None:
            query += " OFFSET ?"
            params.append(offset)

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return tuples_to_dicts(results, self.get_transaction_columns())

    def get_transaction_columns(self):
        return ["transaction_id", "user_id", "account_id", "category_id", "amount", "transaction_type",
                "description", "date", "created_at", "updated_at", "is_deleted", "account_name", "category_name"]

    def get_transactions_by_date_range(self, user_id, start_date, end_date, limit=None, offset=None):
        query = """
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.date BETWEEN ? AND ? AND transactions.is_deleted = 0
        ORDER BY date DESC
        """

        params = [user_id, start_date, end_date]
        if limit is not None and offset is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return tuples_to_dicts(results, self.get_transaction_columns())

    def get_category_statistics_by_date_range(self, user_id, start_date, end_date):
        self.cursor.execute("""
        SELECT categories.category_name, SUM(transactions.amount) as total_amount
        FROM transactions 
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ? AND transactions.date BETWEEN ? AND ? AND transactions.is_deleted = 0
        GROUP BY categories.category_name
        ORDER BY total_amount DESC;
        """, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def get_total_income(self, user_id, start_date, end_date):
        self.cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND transaction_type = 'Thu nhập' AND date BETWEEN ? AND ? AND is_deleted = 0
        """, (user_id, start_date, end_date))
        return self.cursor.fetchone()[0] or 0  # Nếu không có dữ liệu, trả về 0

    def get_total_expense(self, user_id, start_date, end_date):
        self.cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND transaction_type = 'Chi tiêu' AND date BETWEEN ? AND ? AND is_deleted = 0
        """, (user_id, start_date, end_date))
        return self.cursor.fetchone()[0] or 0

    def get_total_balance(self, user_id):
        """Lấy tổng số dư hiện tại từ tất cả các tài khoản, chỉ tính các tài khoản chưa bị xóa."""
        self.cursor.execute("""
        SELECT SUM(balance) FROM accounts 
        WHERE user_id = ? AND is_deleted = 0
        """, (user_id,))
        return self.cursor.fetchone()[0] or 0
