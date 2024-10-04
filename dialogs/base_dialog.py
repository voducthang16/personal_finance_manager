from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox


class BaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
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
                padding-left: 10px;
                background-color: #292929;
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }

            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: #fff;
                border: none;
                padding: 0;
                margin: 0;
                border-radius: 6px;
            }

            QComboBox::item {
                height: 20px;
                padding: 5px;
                border-radius: 6px;
            }

            QComboBox::item:selected {
                background-color: #2e2e2e;
                color: #fff;
            }

            QComboBox::item:hover {
                background-color: #2e2e2e;
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
                image: url('down_arrow.png');
                width: 10px;
                height: 10px;
                margin: 0px;
                padding: 0px;
                alignment: center;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #fff;
            }

            QPushButton {
                font-size: 16px;
                border-radius: 6px;
                padding: 10px 20px;
                min-width: 100px;
            }

            QPushButton#CancelButton {
                background-color: #e74c3c;
                color: #fff;
            }

            QPushButton#SubmitButton {
                background-color: #5dade2;
                color: #fff;
            }

            QPushButton#CancelButton:hover {
                background-color: #c0392b;
            }

            QPushButton#SubmitButton:hover {
                background-color: #3498db;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

    def create_row(self, label_text, widget):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedHeight(40)
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        row_layout.setStretch(0, 1)
        row_layout.setStretch(1, 3)
        return row_layout

    def show_error_message(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message)
