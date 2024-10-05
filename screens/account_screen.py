from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AccountScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Main layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Set background color for the entire widget
        self.setStyleSheet("""
            QWidget {
                background-color: #292929;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        # Header layout
        header_layout = QHBoxLayout()
        self.layout.addLayout(header_layout)

        # Title label for the account list
        self.title_label = QLabel("Danh Sách Tài Khoản")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
            }
        """)
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Account list area (will display the account frames)
        self.account_list_widget = QWidget()
        self.account_list_layout = QVBoxLayout(self.account_list_widget)
        self.account_list_layout.setSpacing(15)
        self.layout.addWidget(self.account_list_widget)

        # Label displayed when no accounts are available
        self.no_account_label = QLabel("Chưa có tài khoản nào. Vui lòng thêm tài khoản.")
        self.no_account_label.setFont(QFont("Arial", 14))
        self.no_account_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.no_account_label)
        self.no_account_label.setVisible(False)

        # Load accounts on initialize
        self.initialize()

    def initialize(self):
        """Load the accounts and display them."""
        self.load_accounts()

    def load_accounts(self):
        """Fetch accounts from the database and display them as custom widgets."""
        # Clear the layout first
        while self.account_list_layout.count():
            child = self.account_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        accounts = self.main_window.db_manager.get_accounts_for_user(self.main_window.user_info['user_id'])

        if not accounts:
            self.no_account_label.setVisible(True)
        else:
            self.no_account_label.setVisible(False)
            for account in accounts:
                account_id, user_id, account_name, balance, created_at = account
                self.add_account_item(account_name, balance)

    def add_account_item(self, account_name, balance):
        """Add a custom account item to the account list layout."""
        account_frame = QFrame()
        account_frame.setStyleSheet("""
            QFrame {
                background-color: #393939;
                border-radius: 12px;
                padding: 20px;
                margin: 10px;
                border: 1px solid #444;
            }
        """)
        account_layout = QHBoxLayout(account_frame)
        account_frame.setLayout(account_layout)

        # Account Name label styling
        account_name_label = QLabel(account_name)
        account_name_label.setFont(QFont("Arial", 16, QFont.Bold))
        account_name_label.setStyleSheet("color: #ffffff;")
        account_layout.addWidget(account_name_label)

        # Account Balance label styling
        account_balance_label = QLabel(f"{balance:,.0f} VND")
        account_balance_label.setFont(QFont("Arial", 16))
        account_balance_label.setStyleSheet("color: #1abc9c;")
        account_balance_label.setAlignment(Qt.AlignRight)
        account_layout.addWidget(account_balance_label)

        self.account_list_layout.addWidget(account_frame)

    def on_account_added(self):
        """Reload the accounts after one is added."""
        self.load_accounts()

