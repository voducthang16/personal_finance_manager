from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog, QLineEdit, QHBoxLayout, QMessageBox, QTableView
from PyQt5.QtGui import QStandardItemModel


class AccountScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Layout for the account screen
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.no_account_label = QLabel("Chưa có tài khoản nào. Vui lòng thêm tài khoản.")
        self.layout.addWidget(self.no_account_label)

        # QTableView to display accounts
        self.account_table = QTableView(self)
        self.account_table.setVisible(False)
        self.layout.addWidget(self.account_table)

        # Add account button
        self.add_account_button = QPushButton("Thêm tài khoản")
        self.layout.addWidget(self.add_account_button)

        # Connect the button to open the add account dialog
        self.add_account_button.clicked.connect(self.open_add_account_dialog)

        # Initialize table model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Tên tài khoản", "Số dư (VND)"])
        self.account_table.setModel(self.model)

    def initialize(self):
        print("initialize account screen")
        print(self.main_window.user_info)

        # Get accounts from the database and update the UI
        self.load_accounts()

    def load_accounts(self):
        """Load accounts from the database and update the UI"""
        accounts = self.main_window.db_manager.get_accounts_for_user(self.main_window.user_info['user_id'])
        print(accounts)
        #
        # # Clear the current model data
        # self.model.removeRows(0, self.model.rowCount())
        #
        # # Check if there are any accounts
        # if not accounts:
        #     self.no_account_label.setVisible(True)
        #     self.account_table.setVisible(False)
        # else:
        #     # Populate the table with accounts
        #     for account in accounts:
        #         account_name_item = QStandardItem(account[2])
        #         balance_item = QStandardItem(f"{account[3]:,.0f}")
        #         self.model.appendRow([account_name_item, balance_item])
        #
        #     # Hide the no account label and show the table
        #     self.no_account_label.setVisible(False)
        #     self.account_table.setVisible(True)

    def open_add_account_dialog(self):
        """Open dialog to add a new account"""
        dialog = AddAccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            account_name, balance = dialog.get_account_data()

            # Add the account to the database
            self.main_window.finance_manager.add_account(self.main_window.user_info['user_id'], account_name, balance)

            # Reload the accounts to update the UI
            self.load_accounts()


class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Tài khoản")
        self.setFixedSize(400, 200)

        # Set up the dialog UI
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Account name input
        self.account_name_input = QLineEdit(self)
        self.account_name_input.setPlaceholderText("Nhập tên tài khoản")
        self.layout.addWidget(self.account_name_input)

        # Balance input
        self.balance_input = QLineEdit(self)
        self.balance_input.setPlaceholderText("Nhập số dư ban đầu")
        self.layout.addWidget(self.balance_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Hủy")
        self.cancel_button.clicked.connect(self.reject)
        self.submit_button = QPushButton("Lưu")
        self.submit_button.clicked.connect(self.submit)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def submit(self):
        """Handle the submit button"""
        account_name = self.account_name_input.text()
        balance = self.balance_input.text()

        if not account_name or not balance:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            balance = float(balance)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số dư phải là một số.")
            return

        self.accept()

    def get_account_data(self):
        """Get the data entered by the user"""
        return self.account_name_input.text(), float(self.balance_input.text())