from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt


class BaseDialog(QDialog):
    def __init__(self, parent=None, title="Tiêu đề", width=400, height=300):
        super().__init__(parent)
        self.title = title
        self.width = width
        self.height = height
        self.setup_ui()

    def setup_ui(self):
        # Thiết lập kích thước cửa sổ
        self.setFixedSize(self.width, self.height)

        # Áp dụng stylesheet cho QDialog và các thành phần khác, loại bỏ các styles chung cho QPushButton
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
            }

            QLabel {
                color: #fff;
                font-size: 16px;
                background-color: transparent;
            }

            QLineEdit, QComboBox, QDateEdit {
                height: 40px;
                padding-left: 10px;
                color: #fff;;
                border-radius: 6px;
                font-size: 16px;
            }

            QComboBox::item {
                height: 20px;
                padding: 6px;
                border-radius: 6px;
            }

            QComboBox::item:selected {
                background-color: #3a3a3a;
                color: #fff;
            }

            QDateEdit::drop-down,
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 20px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QDateEdit::down-arrow,
            QComboBox::down-arrow {
                image: url('assets/down_arrow.png');
                width: 10px;
                height: 10px;
                margin: 0px;
                padding: 0px;
                alignment: center;
            }
        """)

        # Tạo layout chính
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 0, 20, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        # Header
        self.header_widget = QWidget()
        self.header_widget.setStyleSheet("background-color: transparent;")
        self.header_widget.setFixedHeight(60)
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_widget.setLayout(self.header_layout)

        self.header_label = QLabel(self.title)
        self.header_label.setStyleSheet("""
            font-size: 24px;
        """)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.header_label)
        self.header_layout.addStretch()
        self.main_layout.addWidget(self.header_widget)

        self.divider_top = QLabel()
        self.divider_top.setFixedHeight(1)
        self.divider_top.setStyleSheet("background-color: #292929;")
        self.main_layout.addWidget(self.divider_top)

        # Central widget
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent")
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(16)
        self.content_layout.setContentsMargins(0, 20, 0, 20)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_widget.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_widget)

        self.divider_bottom = QLabel()
        self.divider_bottom.setFixedHeight(1)
        self.divider_bottom.setStyleSheet("background-color: #292929;")
        self.main_layout.addWidget(self.divider_bottom)

        # Footer
        self.footer_widget = QWidget()
        self.footer_widget.setStyleSheet("background-color: transparent;")
        self.footer_widget.setFixedHeight(60)
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setAlignment(Qt.AlignCenter)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_widget.setLayout(self.footer_layout)

        self.footer_layout.addStretch()

        self.cancel_button = QPushButton("Hủy")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.setStyleSheet("""
            QPushButton#CancelButton {
                background-color: #e74c3c;
                color: #fff;
                border: none;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton#CancelButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)

        self.submit_button = QPushButton("Lưu")
        self.submit_button.setObjectName("SubmitButton")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setStyleSheet("""
            QPushButton#SubmitButton {
                background-color: #5dade2;
                color: #fff;
                border: none;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton#SubmitButton:hover {
                background-color: #3498db;
            }
        """)
        self.submit_button.clicked.connect(self.submit)

        self.footer_layout.addWidget(self.cancel_button)
        self.footer_layout.addWidget(self.submit_button)

        self.main_layout.addWidget(self.footer_widget)

    def create_row(self, label_text, widget):
        """
        Tạo một hàng gồm QLabel và widget, trả về QWidget chứa layout này.
        """
        widget.setStyleSheet("background-color: #2a2a2a;")
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        label.setFixedHeight(40)
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        row_layout.setStretch(0, 1)
        row_layout.setStretch(1, 3)
        row_widget.setLayout(row_layout)
        return row_widget

    def show_message_box(self, title, message, icon_type):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        background_color = ""
        hover_color = ""

        if icon_type == QMessageBox.Information:
            background_color = '#28a745'
            hover_color = '#218838'
        elif icon_type == QMessageBox.Warning:
            background_color = '#ffc107'
            hover_color = '#e0a800'
        elif icon_type == QMessageBox.Critical:
            background_color = '#dc3545'
            hover_color = '#c82333'

        style = f"""
            QPushButton {{
                background-color: {background_color};
                color: white;
                border: none;
                padding: 4px 0px;
                border-radius: 6px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        msg_box.setStyleSheet(style)
        msg_box.exec_()

    def show_success_message(self, message):
        self.show_message_box("Thành công", message, QMessageBox.Information)

    def show_error_message(self, message):
        self.show_message_box("Lỗi", message, QMessageBox.Critical)

    def show_warning_message(self, message):
        self.show_message_box("Cảnh báo", message, QMessageBox.Warning)

    def add_content(self, widget):
        self.content_layout.addWidget(widget)

    def submit(self):
        self.accept()
