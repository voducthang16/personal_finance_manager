from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QDoubleValidator

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
        """Xử lý khi người dùng nhấn nút Lưu."""
        data = self.get_account_data()
        account_name = data["account_name"]
        balance = data["balance"]

        if not account_name or not balance:
            self.show_error_message("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            balance_float = float(balance.replace(",", "").replace(" VND", ""))
        except ValueError:
            self.show_error_message("Lỗi", "Số dư phải là một số hợp lệ.")
            return

        if self.account_id:
            self.main_window.db_manager.account_manager.update_account(self.account_id, account_name, balance_float)
        else:
            user_id = self.main_window.user_info['user_id']
            self.main_window.db_manager.account_manager.add_account(user_id, account_name, balance_float)

        self.main_window.display_screen("Tài Khoản")
        self.accept()

    def populate_data(self):
        """Điền dữ liệu vào các trường trong dialog khi chỉnh sửa tài khoản."""
        account_name = self.account_data['account_name']  # Tên tài khoản là phần tử đầu tiên
        balance = self.account_data['balance']  # Số dư là phần tử thứ hai
        # Remove commas and ' VND' to make it compatible with float conversion
        balance_clean = balance.replace(",", "").replace(" VND", "")

        self.account_name_input.setText(account_name)
        self.balance_input.setText(balance_clean)  # Hiển thị số dư dạng số
