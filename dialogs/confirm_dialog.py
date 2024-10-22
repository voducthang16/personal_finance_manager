from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class ConfirmDialog(QDialog):
    def __init__(self, title="Xác nhận", message="Bạn có chắc chắn?", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        self.setup_ui(message)

    def setup_ui(self, message):
        layout = QVBoxLayout(self)

        label = QLabel(message)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 18px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        divider = QLabel()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #292929;")
        layout.addWidget(divider)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addStretch(1)

        self.no_button = self.create_button("Không", "#dc3545", "#c82333", self.reject)
        self.yes_button = self.create_button("Có", "#28a745", "#218838", self.accept)

        button_layout.addWidget(self.no_button)
        button_layout.addWidget(self.yes_button)

    def create_button(self, text, bg_color, hover_color, callback):
        button = QPushButton(text)
        button.setFixedHeight(30)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: #fff;
                border: none;
                border-radius: 6px;
                min-width: 100px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        button.clicked.connect(callback)
        return button
