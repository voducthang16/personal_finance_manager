import sqlite3
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt


class SetupLayout(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Tạo widget form để bao bọc các input và nút
        form_widget = QWidget()
        form_widget.setFixedWidth(600)

        # Layout cho form widget
        form_layout = QVBoxLayout(form_widget)

        form_layout.addLayout(self.create_form_row('Họ và tên:', 'name_input'))
        form_layout.addLayout(self.create_form_row('Email:', 'email_input'))
        form_layout.addLayout(self.create_form_row('Tên tài khoản:', 'account_name_input'))
        form_layout.addLayout(self.create_form_row('Số dư tài khoản:', 'account_balance_input'))

        self.register_button = QPushButton('Đăng ký')
        self.register_button.setFixedHeight(40)
        self.register_button.setStyleSheet("""
            QPushButton {
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

    def create_form_row(self, label_text, input_name):
        label = QLabel(label_text)
        label.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)

        input_field = self.create_styled_input()
        setattr(self, input_name, input_field)

        row_layout = QHBoxLayout()
        row_layout.addWidget(label, 1)  # Tỷ lệ 1
        row_layout.addWidget(input_field, 3)  # Tỷ lệ 3

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
        # Validate all fields are not empty
        if not name or not email or not account_name or not account_balance:
            return "Vui lòng điền tất cả các trường."

        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return "Email không hợp lệ."

        # Validate account balance is a number and greater than 0
        try:
            account_balance = float(account_balance)
            if account_balance <= 0:
                return "Số dư phải lớn hơn 0."
        except ValueError:
            return "Số dư tài khoản phải là một số hợp lệ."

        return None  # No errors

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        account_name = self.account_name_input.text()
        account_balance = self.account_balance_input.text()

        # Validate inputs
        validation_error = self.validate_inputs(name, email, account_name, account_balance)
        if validation_error:
            print(validation_error)  # In a real app, you might want to display a dialog instead
            return

        try:
            # Add user to the database
            self.main_window.db_manager.user_manager.add_user(name, email)

            # Fetch the first user (assumed this is the newly added user)
            user = self.main_window.db_manager.user_manager.get_first_user()
            if user is None:
                print("Không thể tìm thấy người dùng vừa thêm.")
                return

            user_id = user['user_id']

            # Add account with the provided balance
            account_balance_float = float(account_balance)
            result = self.main_window.db_manager.account_manager.add_account(user_id, account_name, account_balance_float)

            if result is not None:
                print(result)  # In case of errors, print or show the error message
                return

            # Update the main window with the new user info
            self.main_window.user_info = self.main_window.get_user_info()

            # Show the main screen after successful registration
            self.main_window.show_main_screen()

        except sqlite3.Error as e:
            print(f"Lỗi khi thêm người dùng hoặc tài khoản: {e}")
