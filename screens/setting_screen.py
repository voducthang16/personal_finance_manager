from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt

from widgets import MessageBoxWidget


class SettingScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.message_box = MessageBoxWidget(self)
        self.is_edit_mode = False
        self.init_ui()

    def initialize(self):
        self.bind_user_info(self.main_window.user_info)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        self.create_header()

        user_widget = self.create_user_input_widgets()

        layout.addWidget(self.header_widget)
        layout.addWidget(user_widget)
        layout.addStretch()
        self.setLayout(layout)

    def create_header(self):
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(10, 0, 10, 0)
        title = QLabel("Quản Lý Tài Khoản", self.header_widget)
        title.setFixedHeight(40)
        title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 24px;
                color: #fff;
            }
        """)
        header_layout.addWidget(title, alignment=Qt.AlignTop)

    def create_user_input_widgets(self):
        self.name_label = QLabel('Tên:')
        self.name_label.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)

        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                padding-left: 10px;
                border-radius: 8px;
                font-size: 16px;
            }
        """)

        self.email_label = QLabel('Email:')
        self.email_label.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)

        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(40)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                padding-left: 10px;
                border-radius: 8px;
                font-size: 16px;
            }
        """)

        self.update_button = QPushButton('Cập nhật thông tin')
        self.update_button.setFixedHeight(40)
        self.update_button.setStyleSheet("""
            QPushButton {
                padding: 0 10px;
                background-color: #5555FF;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #7777FF;
            }
            QPushButton:pressed {
                background-color: #3333AA;
            }
        """)
        self.update_button.clicked.connect(self.update_info)

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label, 1)
        name_layout.addWidget(self.name_input, 3)

        email_layout = QHBoxLayout()
        email_layout.addWidget(self.email_label, 1)
        email_layout.addWidget(self.email_input, 3)

        user_widget = QWidget()
        user_widget.setStyleSheet("""
            QWidget {
                background-color: #292929;
                border-radius: 10px;
                margin: 0 10px;
            }
        """)

        input_layout = QVBoxLayout(user_widget)
        input_layout.addLayout(name_layout)
        input_layout.addLayout(email_layout)
        input_layout.addWidget(self.update_button, alignment=Qt.AlignRight)

        return user_widget

    def bind_user_info(self, user_info):
        if user_info:
            self.name_input.setText(user_info['name'])
            self.email_input.setText(user_info['email'])
            self.is_edit_mode = True
        else:
            self.clear_fields()
            self.is_edit_mode = False

    def update_info(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not email:
            self.message_box.show_error_message("Vui lòng điền đầy đủ thông tin!")
            return

        if self.is_edit_mode:
            try:
                self.main_window.db_manager.user_manager.update_user(self.main_window.user_info['user_id'], name, email)
                self.main_window.user_info = self.main_window.db_manager.user_manager.get_first_user()
                self.message_box.show_success_message("Thông tin đã được cập nhật thành công!")
            except Exception as e:
                self.message_box.show_error_message(f"Lỗi khi cập nhật thông tin: {e}")
        else:
            try:
                self.main_window.db_manager.user_manager.add_user(name, email)
                self.main_window.user_info = self.main_window.db_manager.user_manager.get_first_user()
                self.message_box.show_success_message("Thêm người dùng thành công!")
            except Exception as e:
                self.message_box.show_error_message(f"Lỗi khi thêm người dùng: {e}")

    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
