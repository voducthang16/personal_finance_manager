# custom_modal.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QFormLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QDoubleValidator

class TransactionDialog(QDialog):
    def __init__(self, parent=None, transaction_data=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Giữa Giao dịch")
        self.setWindowIcon(QIcon("icons/transaction.png"))  # Thêm biểu tượng nếu có
        self.setFixedSize(450, 400)
        self.setup_ui()
        self.transaction_data = transaction_data
        if self.transaction_data:
            self.populate_data()

    def setup_ui(self):
        # Đặt nền màu trắng cho dialog và các widget con
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #5DADE2;
                color: black;
            }
            QPushButton {
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton#CancelButton {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton#SubmitButton {
                background-color: #5DADE2;
                color: white;
            }
            QPushButton#CancelButton:hover {
                background-color: #C0392B;
            }
            QPushButton#SubmitButton:hover {
                background-color: #3498DB;
            }
        """)

        # Layout chính
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(20)

        # Số tiền
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Nhập số tiền")
        self.amount_input.setValidator(QDoubleValidator(0.99, 9999999.99, 2))
        form_layout.addRow(QLabel("Số tiền:"), self.amount_input)

        # Loại giao dịch
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Chi tiêu", "Thu nhập", "Vay nợ"])
        form_layout.addRow(QLabel("Loại giao dịch:"), self.type_combo)

        # Hạng mục
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Đồ ăn", "Đi chợ", "Giải trí", "Tiện ích",
            "Di chuyển", "Lương", "Thưởng", "Vay nợ", "Khác"
        ])
        form_layout.addRow(QLabel("Hạng mục:"), self.category_combo)

        # Diễn giải
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Nhập diễn giải")
        form_layout.addRow(QLabel("Diễn giải:"), self.description_input)

        # Ngày giao dịch
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow(QLabel("Ngày giao dịch:"), self.date_edit)

        # Tài khoản
        self.account_combo = QComboBox()
        self.account_combo.addItems(["Tiền mặt", "Tài khoản ngân hàng", "Thẻ tín dụng"])
        form_layout.addRow(QLabel("Tài khoản:"), self.account_combo)

        main_layout.addLayout(form_layout)

        # Divider
        divider = QLabel()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: #CCCCCC;")
        main_layout.addWidget(divider)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Hủy", self)
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.setFixedHeight(40)
        self.cancel_button.clicked.connect(self.reject)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setObjectName("SubmitButton")
        self.submit_button.setFixedHeight(40)
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

# Đoạn mã này cho phép bạn chạy dialog độc lập để kiểm tra giao diện
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TransactionDialog()
    if dialog.exec_() == QDialog.Accepted:
        print(dialog.get_transaction_data())
    sys.exit(app.exec_())
