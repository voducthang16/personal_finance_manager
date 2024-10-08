import sqlite3

from database.account_manager import AccountManager
from database.category_manager import CategoryManager
from database.transaction_manager import TransactionManager
from database.user_manager import UserManager


class FinanceManager:
    def __init__(self, db_name='personal_finance.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Initialize managers
        self.user_manager = UserManager(self.cursor)
        self.account_manager = AccountManager(self.cursor)
        self.category_manager = CategoryManager(self.cursor)
        self.transaction_manager = TransactionManager(self.cursor)

    def create_tables(self):
        """Create necessary tables."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

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

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            category_type TEXT NOT NULL, -- "Thu nhập" hoặc "Chi tiêu"
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

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

    def close(self):
        """Close the database connection."""
        self.conn.close()
