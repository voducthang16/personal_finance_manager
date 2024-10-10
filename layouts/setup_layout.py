import sqlite3

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

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        account_name = self.account_name_input.text()
        account_balance = self.account_balance_input.text()

        if not name or not email or not account_name or not account_balance:
            print("Vui lòng điền tất cả các trường.")
            return

        try:
            self.main_window.db_manager.user_manager.add_user(name, email)

            user = self.main_window.db_manager.user_manager.get_first_user()
            user_id = user['user_id']

            self.main_window.db_manager.account_manager.add_account(user_id, account_name, account_balance)
            self.add_default_categories()

            self.main_window.user_info = self.main_window.get_user_info()

            self.main_window.show_main_screen()
        except sqlite3.Error as e:
            print(f"Lỗi khi thêm người dùng hoặc tài khoản: {e}")

    def add_default_categories(self):
        default_categories = [
            ("Đồ ăn", "Chi tiêu"),
            ("Giải trí", "Chi tiêu"),
            ("Lương", "Thu nhập"),
            ("Mua sắm", "Chi tiêu"),
            ("Tiết kiệm", "Thu nhập"),
            ("Chi phí sinh hoạt", "Chi tiêu"),
        ]

        for category_name, category_type in default_categories:
            self.main_window.db_manager.category_manager.add_category(category_name, category_type)
