# account_dialog.py

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDoubleValidator

from dialogs.base_dialog import BaseDialog


class AccountDialog(BaseDialog):
    def __init__(self, parent=None, account_data=None):
        title = "Thêm Tài Khoản" if account_data is None else "Sửa Tài Khoản"
        width = 600
        height = 600
        super().__init__(parent, title=title, width=width, height=height)
        self.account_data = account_data
        self.setup_account_fields()
        if self.account_data:
            self.populate_data()

    def setup_account_fields(self):
        # Tên tài khoản
        self.account_name_input = QLineEdit()
        self.account_name_input.setFixedHeight(40)
        self.account_name_input.setPlaceholderText("Nhập tên tài khoản")
        self.add_content(self.create_row("Tên tài khoản:", self.account_name_input))

        # Số dư
        self.balance_input = QLineEdit()
        self.balance_input.setFixedHeight(40)
        self.balance_input.setPlaceholderText("Nhập số dư")
        self.balance_input.setValidator(QDoubleValidator(0.00, 1000000000.00, 2))
        self.add_content(self.create_row("Số dư:", self.balance_input))

    def get_account_data(self):
        return {
            "account_name": self.account_name_input.text().strip(),
            "balance": self.balance_input.text().strip()
        }

    def submit(self):
        data = self.get_account_data()
        account_name = data["account_name"]
        balance = data["balance"]

        if not account_name or not balance:
            self.show_error_message("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            self.balance = float(balance)
        except ValueError:
            self.show_error_message("Lỗi", "Số dư phải là một số.")
            return

        super().submit()

    def populate_data(self):
        self.account_name_input.setText(self.account_data.get("account_name", ""))
        self.balance_input.setText(f"{self.account_data.get('balance', 0):.2f}")
