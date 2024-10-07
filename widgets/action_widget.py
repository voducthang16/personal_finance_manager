from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ActionWidget(QWidget):
    def __init__(self, parent=None, edit_callback=None, delete_callback=None, row=None):
        super().__init__(parent)

        # Create buttons
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")

        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;  /* Blue color */
                color: white;  /* Text color */
                border: none;  /* No border */
                border-radius: 4px;  /* Rounded corners */
                padding: 5px 10px;  /* Padding */
            }
            QPushButton:hover {
                background-color: #2980b9;  /* Darker blue on hover */
            }
        """)

        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;  /* Red color */
                color: white;  /* Text color */
                border: none;  /* No border */
                border-radius: 4px;  /* Rounded corners */
                padding: 5px 10px;  /* Padding */
            }
            QPushButton:hover {
                background-color: #c0392b;  /* Darker red on hover */
            }
        """)

        # Connect buttons to their respective callbacks
        self.edit_button.clicked.connect(lambda: edit_callback(row) if edit_callback else None)
        self.delete_button.clicked.connect(lambda: delete_callback(row) if delete_callback else None)

        # Create layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(0, 0, 0, 0)  # Optional: Adjust margins to your preference
        layout.setSpacing(5)

        # Set the layout for this widget
        self.setLayout(layout)
