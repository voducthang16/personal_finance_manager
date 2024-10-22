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
        self.setStyleSheet(self.get_stylesheet())

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 0, 20, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.setup_header()

        self.add_divider()

        self.setup_content()

        self.add_divider()

        self.setup_footer()

    def get_stylesheet(self):
        return """
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

            QCalendarWidget QSpinBox::up-button,
            QCalendarWidget QSpinBox::down-button {
                subcontrol-origin: border;
                width: 16px;
                background-color: #3a3a3a;
            }

            QCalendarWidget QSpinBox::up-button {
                subcontrol-position: top right;
                border-left: 1px solid #3a3a3a;
                border-top-right-radius: 4px;
            }

            QCalendarWidget QSpinBox::down-button {
                subcontrol-position: bottom right;
                border-left: 1px solid #3a3a3a;
                border-bottom-right-radius: 4px;
            }

            QCalendarWidget QSpinBox::up-arrow,
            QCalendarWidget QSpinBox::down-arrow {
                width: 10px;
                height: 10px;
            }

            QCalendarWidget QSpinBox::up-arrow {
                image: url('assets/up_arrow.png');
            }

            QCalendarWidget QSpinBox::down-arrow {
                image: url('assets/down_arrow.png');
            }

            QCalendarWidget QSpinBox::up-button:hover,
            QCalendarWidget QSpinBox::down-button:hover {
                background-color: #5a5a5a;
            }

            QPushButton#CancelButton {
                background-color: #e74c3c;
                color: #fff;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                font-size: 16px;
                height: 40px;
            }
            QPushButton#CancelButton:hover {
                background-color: #c0392b;
            }

            QPushButton#SubmitButton {
                background-color: #5dade2;
                color: #fff;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                font-size: 16px;
                height: 40px;
            }
            QPushButton#SubmitButton:hover {
                background-color: #3498db;
            }
        """

    def setup_header(self):
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: transparent;")
        header_widget.setFixedHeight(60)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_widget.setLayout(header_layout)

        header_label = QLabel(self.title)
        header_label.setStyleSheet("font-size: 24px;")
        header_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(header_label)
        header_layout.addStretch()
        self.main_layout.addWidget(header_widget)

    def add_divider(self):
        divider = QLabel()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #292929;")
        self.main_layout.addWidget(divider)

    def setup_content(self):
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout()
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(0, 20, 0, 20)
        content_layout.setAlignment(Qt.AlignTop)
        content_widget.setLayout(content_layout)
        self.main_layout.addWidget(content_widget)
        self.content_layout = content_layout

    def setup_footer(self):
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: transparent;")
        footer_widget.setFixedHeight(60)

        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_widget.setLayout(footer_layout)

        cancel_button = self.create_button("Hủy", "CancelButton", self.reject)
        submit_button = self.create_button("Lưu", "SubmitButton", self.submit)

        footer_layout.addStretch()
        footer_layout.addWidget(cancel_button)
        footer_layout.addWidget(submit_button)
        footer_layout.addStretch()

        self.main_layout.addWidget(footer_widget)

    def create_button(self, text, object_name, callback):
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setFixedHeight(40)
        button.clicked.connect(callback)
        return button

    def create_row(self, label_text, widget):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        label.setFixedHeight(40)

        widget.setStyleSheet("background-color: #2a2a2a;")

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
