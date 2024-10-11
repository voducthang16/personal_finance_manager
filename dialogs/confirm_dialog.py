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
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Divider
        divider = QLabel()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #292929;")
        layout.addWidget(divider)

        # Footer layout cho nút
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Căn các nút qua bên phải
        button_layout.addStretch(1)

        self.no_button = QPushButton("No")
        self.no_button.setFixedHeight(30)
        self.no_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.no_button.clicked.connect(self.reject)
        button_layout.addWidget(self.no_button)

        self.yes_button = QPushButton("Yes")
        self.yes_button.setFixedHeight(30)
        self.yes_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.yes_button.clicked.connect(self.accept)
        button_layout.addWidget(self.yes_button)
