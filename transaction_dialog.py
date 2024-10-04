# custom_modal.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QDoubleValidator


class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction_data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Giữa Giao dịch")
        self.setFixedSize(600, 600)
        self.setup_ui()
        self.transaction_data = transaction_data
        if self.transaction_data:
            self.populate_data()

    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #000;
            }

            QLabel {
                color: #fff;
                font-size: 16px;
                background-color: transparent;
            }

            QLineEdit, QComboBox, QDateEdit {
                padding-left: 10px;
                background-color: #121212;
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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Row layout helper function
        def create_row(label_text, widget):
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedHeight(40)
            row_layout.addWidget(label)
            row_layout.addWidget(widget)
            row_layout.setStretch(0, 1)
            row_layout.setStretch(1, 3)
            return row_layout

        # Số tiền input field
        self.amount_input = QLineEdit()
        self.amount_input.setFixedHeight(40)
        self.amount_input.setPlaceholderText("Nhập số tiền")
        self.amount_input.setValidator(QDoubleValidator(0.99, 9999999.99, 2))
        main_layout.addLayout(create_row("Số tiền:", self.amount_input))

        # Loại giao dịch dropdown
        self.type_combo = QComboBox()
        self.type_combo.setFixedHeight(40)
        self.type_combo.addItems(["Chi tiêu", "Thu nhập", "Vay nợ"])
        main_layout.addLayout(create_row("Loại giao dịch:", self.type_combo))

        # Hạng mục dropdown
        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(40)
        self.category_combo.addItems([
            "Đồ ăn", "Đi chợ", "Giải trí", "Tiện ích",
            "Di chuyển", "Lương", "Thưởng", "Vay nợ", "Khác"
        ])
        main_layout.addLayout(create_row("Hạng mục:", self.category_combo))

        # Diễn giải input field
        self.description_input = QLineEdit()
        self.description_input.setFixedHeight(40)
        self.description_input.setPlaceholderText("Nhập diễn giải")
        main_layout.addLayout(create_row("Diễn giải:", self.description_input))

        # Ngày giao dịch field with a calendar popup
        self.date_edit = QDateEdit()
        self.date_edit.setFixedHeight(40)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        main_layout.addLayout(create_row("Ngày giao dịch:", self.date_edit))

        # Tài khoản dropdown
        self.account_combo = QComboBox()
        self.account_combo.setFixedHeight(40)
        self.account_combo.addItems(["Tiền mặt", "Tài khoản ngân hàng", "Thẻ tín dụng"])
        main_layout.addLayout(create_row("Tài khoản:", self.account_combo))

        # Divider for buttons
        divider = QLabel()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #444444;")
        main_layout.addWidget(divider)

        # Buttons for actions
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.cancel_button = QPushButton("Hủy", self)
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setFixedHeight(45)
        self.cancel_button.clicked.connect(self.reject)

        self.submit_button = QPushButton("Lưu", self)
        self.submit_button.setObjectName("SubmitButton")
        self.submit_button.setFixedHeight(45)
        self.submit_button.clicked.connect(self.submit)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.submit_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_transaction_data(self):
        return {
            "amount": self.amount_input.text(),
            "type": self.type_combo.currentText(),
            "category": self.category_combo.currentText(),
            "description": self.description_input.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "account": self.account_combo.currentText()
        }

    def submit(self):
        data = self.get_transaction_data()
        print("Giao dịch mới:", data)
        self.accept()

    def populate_data(self):
        self.amount_input.setText(self.transaction_data.get("amount", ""))
        self.type_combo.setCurrentText(self.transaction_data.get("type", "Chi tiêu"))
        self.category_combo.setCurrentText(self.transaction_data.get("category", "Đồ ăn"))
        self.description_input.setText(self.transaction_data.get("description", ""))
        date_str = self.transaction_data.get("date", QDate.currentDate().toString("yyyy-MM-dd"))
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        if date.isValid():
            self.date_edit.setDate(date)
        self.account_combo.setCurrentText(self.transaction_data.get("account", "Tiền mặt"))


# Đoạn mã này giúp chạy dialog độc lập để kiểm tra giao diện
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TransactionDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("exit")
    sys.exit(app.exec_())
