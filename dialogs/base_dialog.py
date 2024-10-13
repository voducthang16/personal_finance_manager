from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt5.QtCore import Qt

from widgets import MessageBoxWidget


class BaseDialog(QDialog):
    def __init__(self, parent=None, title="Tiêu đề", width=400, height=300):
        super().__init__(parent)
        self.message_box = MessageBoxWidget(self)
        self.title = title
        self.width = width
        self.height = height
        self.setWindowTitle("Personal Finance Manager")
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(self.width, self.height)

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
                color: #fff;
                border-radius: 6px;
                font-size: 16px;
                background-color: #1e1e1e;
                border: 1px solid #3a3a3a;
            }
            
            QComboBox::item, QDateEdit::item {
                height: 20px;
                padding: 6px;
                border-radius: 6px;
            }
            
            QComboBox::item:selected, QDateEdit::item:selected {
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
                margin-right: 5px;
            }
            
            QCalendarWidget {
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                color: white;
                min-width: 300px;
                max-width: 300px;
                min-height: 200px;
            }
            
            QCalendarWidget QWidget {
                alternate-background-color: #1e1e1e;
            }
            
            QCalendarWidget QAbstractItemView:enabled {
                color: #ffffff;
                background-color: #2b2b2b;
                selection-background-color: #3498db;
                selection-color: white;
            }
            
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #1e1e1e;
                padding: 4px;
            }
            
            QCalendarWidget QToolButton {
                color: #ffffff;
                background-color: #3a3a3a;
                border: none;
                border-radius: 4px;
                margin: 2px;
                padding: 4px;
            }
            
            QCalendarWidget QToolButton:hover {
                background-color: #5a5a5a;
            }
            
            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }
            
            QCalendarWidget #qt_calendar_monthbutton, 
            QCalendarWidget #qt_calendar_yearbutton {
                padding: 0px 10px;
                margin: 0px 3px;
            }
            
            QCalendarWidget QMenu {
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                color: white;
            }
            
            QCalendarWidget QMenu::item:selected {
                background-color: #3498db;
            }
            
            QCalendarWidget QSpinBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 2px;
                margin: 0px 3px;
            }
            
            QCalendarWidget QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left: 1px solid #3a3a3a;
                border-top-right-radius: 4px;
                background-color: #3a3a3a;
            }
            
            QCalendarWidget QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left: 1px solid #3a3a3a;
                border-bottom-right-radius: 4px;
                background-color: #3a3a3a;
            }
            
            QCalendarWidget QSpinBox::up-arrow {
                image: url('assets/up_arrow.png');
                width: 10px;
                height: 10px;
            }
            
            QCalendarWidget QSpinBox::down-arrow {
                image: url('assets/down_arrow.png');
                width: 10px;
                height: 10px;
            }
            
            QCalendarWidget QSpinBox::up-button:hover,
            QCalendarWidget QSpinBox::down-button:hover {
                background-color: #5a5a5a;
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
                font-size: 16px;
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
                font-size: 16px;
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

    def add_content(self, widget):
        self.content_layout.addWidget(widget)

    def submit(self):
        self.accept()
