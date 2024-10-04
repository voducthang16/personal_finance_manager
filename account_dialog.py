# account_dialog.py

from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QDoubleValidator

from dialogs.base_dialog import BaseDialog


class AccountDialog(BaseDialog):
    def __init__(self, parent=None, account_data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa Tài khoản")
        self.setFixedSize(400, 200)
        self.account_data = account_data
        self.setup_account_fields()
        if self.account_data:
            self.populate_data()

    def setup_account_fields(self):
        # Account name input
        self.account_name_input = QLineEdit()
        self.account_name_input.setPlaceholderText("Nhập tên tài khoản")
        self.main_layout.addLayout(self.create_row("Tên tài khoản:", self.account_name_input))

        # Balance input
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Nhập số dư")
        self.balance_input.setValidator(QDoubleValidator(0.00, 1000000000.00, 2))
        self.main_layout.addLayout(self.create_row("Số dư:", self.balance_input))

        # Buttons for actions
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.cancel_button = QPushButton("Hủy", self)
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setFixedHeight(45)
        self.cancel_button.clicked.connect(self.reject)

        self.submit_button = QPushButton("Lưu", self)
        self.submit_button.setObjectName("SubmitButton")
        self.submit_button.setFixedHeight(45)
        self.submit_button.clicked.connect(self.submit)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.submit_button)

        self.main_layout.addLayout(button_layout)

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

        self.accept()

    def populate_data(self):
        self.account_name_input.setText(self.account_data.get("account_name", ""))
        self.balance_input.setText(f"{self.account_data.get('balance', 0):.2f}")
