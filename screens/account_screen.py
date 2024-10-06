from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout
)
from PyQt5.QtCore import Qt

from widgets.table_widget import TableWidget


class AccountScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setContentsMargins(10, 0, 10, 0)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.create_header()

        # Table widget to display account information
        self.table_widget = TableWidget()
        self.layout.addWidget(self.table_widget)

    def initialize(self):
        """Ensure the table widget and data are reset when visiting again."""
        self.table_widget.initialize()  # Clear previous data and reset the table
        self.load_accounts()  # Load accounts again

    def create_header(self):
        title = QLabel("Quản Lý Tài Khoản", self)
        title.setFixedHeight(40)
        title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 24px;
                color: #fff;
            }
        """)
        self.layout.addWidget(title)

    def load_accounts(self):
        """Load account data and populate the table."""
        # You may need to fetch accounts from your database manager like this:
        # accounts = self.main_window.db_manager.get_accounts_for_user(self.main_window.user_info['user_id'])

        # Example account data
        accounts = [
            ["Savings Account", "5,000,000 VND", "2024-10-01"],
            ["Credit Card", "1,200,000 VND", "2024-09-25"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
            ["Investment Account", "12,000,000 VND", "2024-10-05"],
        ]

        # Define the headers for the accounts table
        headers = ["Account Name", "Balance", "Last Updated"]

        # Pass both headers and accounts data to the table widget
        self.table_widget.set_data(headers, accounts)

    def add_account_item(self, account_name, balance):
        """Add a custom account item to the table widget."""
        self.table_widget.add_row([account_name, balance])

    def on_account_added(self):
        """Reload the accounts after one is added."""
        self.load_accounts()
