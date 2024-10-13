from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ActionWidget(QWidget):
    def __init__(self, parent=None, edit_callback=None, delete_callback=None, row=None):
        super().__init__(parent)

        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")

        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;;
            }
        """)

        self.edit_button.clicked.connect(lambda: edit_callback(row) if edit_callback else None)
        self.delete_button.clicked.connect(lambda: delete_callback(row) if delete_callback else None)

        # Create layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        # Set the layout for this widget
        self.setLayout(layout)
