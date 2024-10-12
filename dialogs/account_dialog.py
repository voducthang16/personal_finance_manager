from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDoubleValidator

from constants import SCREEN_NAMES
from dialogs.base_dialog import BaseDialog


class AccountDialog(BaseDialog):
    def __init__(self, main_window=None, account_data=None):
        self.account_id = account_data['account_id'] if account_data else None
        title = "Sửa Tài Khoản" if self.account_id else "Thêm Tài Khoản"
        width = 600
        height = 600
        super().__init__(main_window, title=title, width=width, height=height)
        self.main_window = main_window
        self.account_data = account_data
        self.setup_account_fields()
        if self.account_data:
            self.populate_data()

    def setup_account_fields(self):
        self.account_name_input = QLineEdit()
        self.account_name_input.setFixedHeight(40)
        self.account_name_input.setPlaceholderText("Nhập tên tài khoản")
        self.add_content(self.create_row("Tên tài khoản:", self.account_name_input))

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
            self.show_error_message("Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            balance_float = float(balance.replace(",", "").replace(" VND", ""))
        except ValueError:
            self.message_box.show_error_message("Số dư phải là một số hợp lệ.")
            return

        if self.account_id:
            self.main_window.db_manager.account_manager.update_account(self.account_id, account_name, balance_float)
            self.message_box.show_success_message("Cập nhật tài khoản thành công.")
        else:
            user_id = self.main_window.user_info['user_id']
            self.main_window.db_manager.account_manager.add_account(user_id, account_name, balance_float)
            self.message_box.show_success_message("Thêm tài khoản thành công.")

        self.main_window.display_screen(SCREEN_NAMES["ACCOUNT"])
        self.accept()

    def populate_data(self):
        self.account_name_input.setText(self.account_data.get("account_name", ""))
        self.balance_input.setText(str(self.account_data.get("balance", "")))
