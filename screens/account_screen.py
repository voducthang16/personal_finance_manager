from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout
)
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
        self.table_widget.initialize()
        self.load_accounts()

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

    def format_accounts_data(self, accounts_raw):
        formatted_data = []
        for account in accounts_raw:
            account_id, user_id, account_name, balance, last_updated = account
            balance_formatted = f"{balance:,.0f} VND"  # Định dạng số dư
            last_updated_formatted = last_updated.split()[0]  # Chỉ lấy ngày
            formatted_data.append([account_name, balance_formatted, last_updated_formatted])
        return formatted_data

    def load_accounts(self):
        """Load account data and populate the table."""
        # You may need to fetch accounts from your database manager like this:
        accounts = self.main_window.db_manager.get_accounts_for_user(self.main_window.user_info['user_id'])
        accounts_formatted = self.format_accounts_data(accounts)

        # Define the headers for the accounts table
        headers = ["Account Name", "Balance", "Last Updated"]

        # Pass both headers and accounts data to the table widget
        self.table_widget.set_data(headers, accounts_formatted)

    def add_account_item(self, account_name, balance):
        """Add a custom account item to the table widget."""
        self.table_widget.add_row([account_name, balance])

    def on_account_added(self):
        """Reload the accounts after one is added."""
        self.load_accounts()
