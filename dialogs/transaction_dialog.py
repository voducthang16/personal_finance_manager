from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDoubleValidator

from dialogs.base_dialog import BaseDialog
from utils.toast import QToast


class TransactionDialog(BaseDialog):
    def __init__(self, parent=None, transaction_data=None, accounts=None, categories=None):
        super().__init__(
            parent,
            title="Thêm/Chỉnh Sửa Giao dịch",  # Đặt tiêu đề thông qua BaseDialog
            width=600,
            height=600
        )
        self.transaction_data = transaction_data
        self.accounts = accounts if accounts else []
        self.categories = categories if categories else []
        self.setup_transaction_fields()
        if self.transaction_data:
            self.populate_data()

    def setup_transaction_fields(self):
        # Số tiền input field
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Nhập số tiền")
        self.amount_input.setValidator(QDoubleValidator(0.99, 9999999.99, 2))
        self.add_content(self.create_row("Số tiền:", self.amount_input))

        # Loại giao dịch dropdown
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Chi tiêu", "Thu nhập", "Vay nợ"])
        self.type_combo.currentTextChanged.connect(self.update_category_options)
        self.add_content(self.create_row("Loại giao dịch:", self.type_combo))

        # Hạng mục dropdown
        self.category_combo = QComboBox()
        self.populate_categories()
        self.add_content(self.create_row("Hạng mục:", self.category_combo))

        # Diễn giải input field
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Nhập diễn giải")
        self.add_content(self.create_row("Diễn giải:", self.description_input))

        # Ngày giao dịch field với popup lịch
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.add_content(self.create_row("Ngày giao dịch:", self.date_edit))

        # Tài khoản dropdown
        self.account_combo = QComboBox()
        self.populate_accounts()
        self.add_content(self.create_row("Tài khoản:", self.account_combo))

    def populate_accounts(self):
        self.account_combo.clear()
        for account in self.accounts:
            self.account_combo.addItem(account['account_name'], account['account_id'])

    def populate_categories(self):
        self.category_combo.clear()
        for category in self.categories:
            self.category_combo.addItem(category['category_name'], category['category_id'])

    def update_category_options(self, transaction_type):
        self.category_combo.clear()
        filtered_categories = [
            cat for cat in self.categories if cat.get('category_type') == transaction_type
        ]
        for category in filtered_categories:
            self.category_combo.addItem(category['category_name'], category['category_id'])

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
        amount = data["amount"]
        transaction_type = data["type"]
        category = data["category"]
        description = data["description"]
        date = data["date"]
        account = data["account"]

        # Kiểm tra các trường bắt buộc
        if not amount or not transaction_type or not category or not account:
            self.toast(
                title="Cảnh báo",
                message="Vui lòng nhập đầy đủ thông tin.",
                toast_type=QToast.WARNING,
                duration=3000
            )
            return

        try:
            self.amount = float(amount)
        except ValueError:
            self.toast(
                title="Lỗi",
                message="Số tiền phải là một số hợp lệ.",
                toast_type=QToast.ERROR,
                duration=3000
            )
            return

        # Nếu mọi thứ đều hợp lệ, bạn có thể xử lý dữ liệu ở đây
        # Ví dụ: Lưu giao dịch vào cơ sở dữ liệu
        # ...

        self.accept()

    def populate_data(self):
        self.amount_input.setText(str(self.transaction_data.get("amount", "")))
        self.type_combo.setCurrentText(self.transaction_data.get("type", "Chi tiêu"))
        self.populate_categories()
        self.category_combo.setCurrentText(self.transaction_data.get("category", "Đồ ăn"))
        self.description_input.setText(self.transaction_data.get("description", ""))

        date_str = self.transaction_data.get("date", QDate.currentDate().toString("yyyy-MM-dd"))
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        if date.isValid():
            self.date_edit.setDate(date)

        self.account_combo.setCurrentText(self.transaction_data.get("account", "Tiền mặt"))
