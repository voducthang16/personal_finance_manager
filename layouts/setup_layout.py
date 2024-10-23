import sqlite3
import re

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

from widgets import MessageBoxWidget


class SetupLayout(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.message_box = MessageBoxWidget(self.main_window)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                border-radius: 10px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        form_widget = QWidget()
        form_widget.setFixedWidth(600)

        form_layout = QVBoxLayout(form_widget)

        form_layout.addLayout(self.create_form_row('Họ và tên:', 'name_input'))
        form_layout.addLayout(self.create_form_row('Email:', 'email_input'))
        form_layout.addLayout(self.create_form_row('Tên tài khoản:', 'account_name_input'))
        form_layout.addLayout(self.create_form_row('Số dư tài khoản:', 'account_balance_input', True))

        self.register_button = QPushButton('Thiết lập')
        self.register_button.setFixedHeight(40)
        self.register_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 0 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3333AA;
            }
        """)
        self.register_button.clicked.connect(self.register)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer)
        form_layout.addWidget(self.register_button, alignment=Qt.AlignRight)

        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def create_form_row(self, label_text, input_name, is_number=False):
        label = QLabel(label_text)
        label.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)

        input_field = self.create_styled_input()
        setattr(self, input_name, input_field)

        if is_number:
            input_field.setValidator(QIntValidator(0, 1000000000))

        row_layout = QHBoxLayout()
        row_layout.addWidget(label, 1)
        row_layout.addWidget(input_field, 3)

        return row_layout

    def create_styled_input(self):
        input_field = QLineEdit()
        input_field.setFixedHeight(40)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: #fff;
                border: 1px solid #fff;
                border-radius: 6px;
                padding-left: 10px;
            }
        """)
        return input_field

    def validate_inputs(self, name, email, account_name, account_balance):
        if not name or not email or not account_name or not account_balance:
            return "Vui lòng điền tất cả các trường"

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return "Email không hợp lệ"

        if not re.match(r"^\d+$", account_balance):
            return "Số dư phải là một số nguyên hợp lệ"

        try:
            account_balance = int(account_balance)
            if account_balance <= 0:
                return "Số dư phải lớn hơn 0"
        except ValueError:
            return "Số dư tài khoản phải là một số hợp lệ"

        return None

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        account_name = self.account_name_input.text()
        account_balance = self.account_balance_input.text()

        validation_error = self.validate_inputs(name, email, account_name, account_balance)
        if validation_error:
            self.message_box.show_error_message(validation_error)
            return

        try:
            self.main_window.db_manager.user_manager.add_user(name, email)

            user = self.main_window.db_manager.user_manager.get_first_user()

            user_id = user['user_id']

            account_balance_float = float(account_balance)
            result = self.main_window.db_manager.account_manager.add_account(user_id, account_name, account_balance_float)

            self.main_window.user_info = self.main_window.get_user_info()

            self.main_window.setup_window_property()
            self.main_window.show_main_screen()

        except sqlite3.Error as e:
            self.message_box.show_error_message(f"Lỗi khi thêm người dùng hoặc tài khoản: {e}")
