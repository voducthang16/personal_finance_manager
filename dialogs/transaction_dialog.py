from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDoubleValidator

from dialogs.base_dialog import BaseDialog


class TransactionDialog(BaseDialog):
    def __init__(self, main_window=None, transaction_data=None):
        self.transaction_id = transaction_data['transaction_id'] if transaction_data else None
        title = "Sửa Giao dịch" if self.transaction_id else "Thêm Giao dịch"
        width = 600
        height = 600
        super().__init__(main_window, title=title, width=width, height=height)
        self.transaction_data = transaction_data
        self.main_window = main_window
        self.accounts = []
        self.categories = []
        self.setup_transaction_fields()
        self.populate_accounts()
        self.populate_categories()
        if self.transaction_data:
            self.populate_data()

    def setup_transaction_fields(self):
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Nhập số tiền")
        self.amount_input.setValidator(QDoubleValidator(0.99, 9999999.99, 2))
        self.add_content(self.create_row("Số tiền:", self.amount_input))

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Chi tiêu", "Thu nhập"])
        self.type_combo.currentTextChanged.connect(self.update_category_options)
        self.add_content(self.create_row("Loại giao dịch:", self.type_combo))

        self.category_combo = QComboBox()
        self.add_content(self.create_row("Danh mục:", self.category_combo))

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Nhập diễn giải")
        self.add_content(self.create_row("Diễn giải:", self.description_input))

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.add_content(self.create_row("Ngày giao dịch:", self.date_edit))

        self.account_combo = QComboBox()
        self.add_content(self.create_row("Tài khoản:", self.account_combo))

    def populate_accounts(self):
        self.account_combo.clear()
        user_id = self.main_window.user_info['user_id']
        limit = 100
        offset = 0

        accounts = self.main_window.db_manager.account_manager.get_accounts_for_user(user_id, limit, offset)
        for account in accounts:
            self.account_combo.addItem(account['account_name'], account['account_id'])

    def populate_categories(self):
        self.category_combo.clear()
        limit = 100
        offset = 0
        self.categories = self.main_window.db_manager.category_manager.get_categories(limit, offset)

        if not self.transaction_id:
            transaction_type = "Chi tiêu"
        else:
            transaction_type = self.transaction_data.get('transaction_type', "Chi tiêu")

        filtered_categories = [
            cat for cat in self.categories if cat.get('category_type') == transaction_type
        ]
        for category in filtered_categories:
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
            "transaction_type": self.type_combo.currentText(),
            "category_id": self.category_combo.currentData(),
            "description": self.description_input.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "account_id": self.account_combo.currentData()
        }

    def submit(self):
        data = self.get_transaction_data()
        amount = data["amount"]
        transaction_type = data["transaction_type"]
        category_id = data["category_id"]
        description = data["description"]
        date = data["date"]
        account_id = data["account_id"]

        if not amount or not transaction_type or not category_id or not account_id:
            self.message_box.show_error_message("Vui lòng nhập đầy đủ thông tin")
            return

        try:
            amount_int = int(amount.replace(",", "").replace(" VND", ""))
        except ValueError:
            self.message_box.show_error_message("Số tiền phải là một số")
            return

        if self.transaction_id:
            self.main_window.db_manager.transaction_manager.update_transaction(
                transaction_id=self.transaction_id,
                amount=amount_int,
                transaction_type=transaction_type,
                category_id=category_id,
                account_id=account_id,
                description=description,
                date=date
            )
            self.message_box.show_success_message("Cập nhật giao dịch thành công")
        else:
            user_id = self.main_window.user_info['user_id']
            self.main_window.db_manager.transaction_manager.add_transaction(
                user_id=user_id,
                account_id=account_id,
                category_id=category_id,
                amount=amount_int,
                transaction_type=transaction_type,
                description=description,
                date=date,
            )
            self.message_box.show_success_message("Thêm giao dịch thành công")

        self.main_window.refresh_current_screen()
        self.accept()

    def populate_data(self):
        self.amount_input.setText(str(self.transaction_data.get("amount", "")))
        self.type_combo.setCurrentText(self.transaction_data.get("transaction_type", "Chi tiêu"))
        self.populate_categories()
        self.category_combo.setCurrentText(self.transaction_data.get("category_name", ""))
        self.description_input.setText(self.transaction_data.get("description", ""))

        date_str = self.transaction_data.get("date", QDate.currentDate().toString("yyyy-MM-dd"))
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        if date.isValid():
            self.date_edit.setDate(date)

        self.account_combo.setCurrentText(self.transaction_data.get("account_name", ""))