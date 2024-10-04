import sqlite3


class FinanceManager:
    def __init__(self, db_name='personal_finance.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Tạo các bảng cần thiết cho ứng dụng"""

        # Bảng users (người dùng)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Bảng accounts (tài khoản của người dùng - không có account_type)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_name TEXT NOT NULL,
            balance REAL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """)

        # Bảng categories (danh mục thu nhập hoặc chi tiêu - không có user_id)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            category_type TEXT NOT NULL, -- "Thu nhập" hoặc "Chi tiêu"
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Bảng transactions (giao dịch)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_id INTEGER,
            category_id INTEGER,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL, -- "Thu nhập" hoặc "Chi tiêu"
            description TEXT,
            date TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (account_id) REFERENCES accounts(account_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """)

        self.conn.commit()

    ### Các phương thức để quản lý người dùng, tài khoản, danh mục và giao dịch
    def get_first_user(self):
        self.cursor.execute("SELECT * FROM users ORDER BY user_id ASC LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'created_at': row[3]
            }
        return None

    # Thêm người dùng mới
    def add_user(self, name, email):
        try:
            self.cursor.execute("""
            INSERT INTO users (name, email)
            VALUES (?, ?)
            """, (name, email))  # Sử dụng 2 placeholders cho name và email
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm người dùng: {e}")
            raise e  # Ném lại ngoại lệ để xử lý ở nơi gọi

    def update_user(self, user_id, name, email):
        try:
            self.cursor.execute("""
            UPDATE users 
            SET name = ?, email = ?
            WHERE user_id = ?
            """, (name, email, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật người dùng: {e}")
            raise e

    def get_accounts_for_user(self, user_id):
        """Lấy danh sách tài khoản của người dùng"""
        self.cursor.execute("""
        SELECT * FROM accounts WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()

    # Thêm tài khoản cho người dùng
    def add_account(self, user_id, account_name, balance=0):
        try:
            self.cursor.execute("""
            INSERT INTO accounts (user_id, account_name, balance)
            VALUES (?, ?, ?)
            """, (user_id, account_name, balance))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm tài khoản: {e}")

    # New method to edit an account
    def edit_account(self, account_id, account_name, balance):
        try:
            self.cursor.execute("""
                UPDATE accounts 
                SET account_name = ?, balance = ?
                WHERE account_id = ?
            """, (account_name, balance, account_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi chỉnh sửa tài khoản: {e}")
            raise e  # Re-raise exception for higher-level handling

    # New method to delete an account
    def delete_account(self, account_id):
        try:
            self.cursor.execute("""
                DELETE FROM accounts 
                WHERE account_id = ?
            """, (account_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi xóa tài khoản: {e}")
            raise e  # Re-raise exception for higher-level handling

    # Thêm danh mục
    def add_category(self, category_name, category_type):
        try:
            self.cursor.execute("""
            INSERT INTO categories (category_name, category_type)
            VALUES (?, ?)
            """, (category_name, category_type))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm danh mục: {e}")

    # Thêm giao dịch mới
    def add_transaction(self, user_id, account_id, category_id, amount, transaction_type, description, date):
        try:
            self.cursor.execute("""
            INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, account_id, category_id, amount, transaction_type, description, date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm giao dịch: {e}")

    # Lấy tất cả các giao dịch của người dùng
    def get_all_transactions(self, user_id):
        self.cursor.execute("""
        SELECT transactions.*, accounts.account_name, categories.category_name 
        FROM transactions 
        JOIN accounts ON transactions.account_id = accounts.account_id
        JOIN categories ON transactions.category_id = categories.category_id
        WHERE transactions.user_id = ?
        """, (user_id,))
        return self.cursor.fetchall()

    # Cập nhật giao dịch
    def update_transaction(self, transaction_id, amount, transaction_type, description, date):
        try:
            self.cursor.execute("""
            UPDATE transactions 
            SET amount = ?, transaction_type = ?, description = ?, date = ?
            WHERE transaction_id = ?
            """, (amount, transaction_type, description, date, transaction_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi cập nhật giao dịch: {e}")

    # Xoá giao dịch
    def delete_transaction(self, transaction_id):
        try:
            self.cursor.execute("""
            DELETE FROM transactions WHERE transaction_id = ?
            """, (transaction_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Lỗi khi xoá giao dịch: {e}")

    # Đóng kết nối cơ sở dữ liệu
    def close(self):
        self.conn.close()
