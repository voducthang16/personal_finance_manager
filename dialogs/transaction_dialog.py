from PyQt5.QtWidgets import QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDoubleValidator

from dialogs.base_dialog import BaseDialog
from utils.toast import QToast


class TransactionDialog(BaseDialog):
    def __init__(self, parent=None, transaction_data=None, db_manager=None):
        super().__init__(
            parent,
            title="Thêm/Chỉnh Sửa Giao dịch",
            width=600,
            height=600
        )
        self.transaction_data = transaction_data
        self.parent = parent
        self.db_manager = db_manager
        self.accounts = []  # Placeholder for account data
        self.categories = []  # Placeholder for categories
        self.setup_transaction_fields()
        self.populate_accounts()  # Populate accounts from the database
        self.populate_categories()  # Populate categories from the database
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
        self.add_content(self.create_row("Tài khoản:", self.account_combo))

    def populate_accounts(self):
        """Lấy danh sách tài khoản từ cơ sở dữ liệu và thêm vào dropdown."""
        self.account_combo.clear()
        user_id = self.parent.user_info['user_id']  # Lấy user_id từ thông tin người dùng
        limit = 100  # Giới hạn số tài khoản lấy về
        offset = 0  # Thay đổi offset nếu cần thiết để phân trang

        accounts = self.db_manager.account_manager.get_accounts_for_user(user_id, limit, offset)  # Gọi phương thức với đủ tham số
        for account in accounts:
            self.account_combo.addItem(account['account_name'], account['account_id'])

    def populate_categories(self):
        """Lấy danh sách các danh mục từ cơ sở dữ liệu và thêm vào dropdown."""
        self.category_combo.clear()
        self.categories = self.db_manager.category_manager.get_categories()  # Gọi phương thức để lấy danh mục từ DB
        for category in self.categories:
            self.category_combo.addItem(category['category_name'], category['category_id'])

    def update_category_options(self, transaction_type):
        """Cập nhật hạng mục dựa trên loại giao dịch."""
        self.category_combo.clear()
        filtered_categories = [
            cat for cat in self.categories if cat.get('category_type') == transaction_type
        ]
        for category in filtered_categories:
            self.category_combo.addItem(category['category_name'], category['category_id'])

    def get_transaction_data(self):
        """Trả về dữ liệu giao dịch dưới dạng dictionary."""
        return {
            "amount": self.amount_input.text(),
            "type": self.type_combo.currentText(),
            "category": self.category_combo.currentText(),
            "description": self.description_input.text(),
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "account": self.account_combo.currentText()
        }

    def submit(self):
        """Xử lý khi người dùng nhấn nút Lưu."""
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
        if self.transaction_data:  # Nếu có dữ liệu giao dịch hiện tại, thực hiện cập nhật
            self.db_manager.update_transaction(
                self.transaction_data['transaction_id'],  # Giả định bạn có ID giao dịch
                amount,
                transaction_type,
                description,
                date,
                account
            )
        else:  # Nếu không có dữ liệu giao dịch, thực hiện thêm mới
            user_id = self.parent.user_info['user_id']
            self.db_manager.add_transaction(
                user_id=user_id,
                account_id=self.account_combo.currentData(),  # Lấy account_id từ dropdown
                category_id=self.category_combo.currentData(),  # Lấy category_id từ dropdown
                amount=amount,
                transaction_type=transaction_type,
                description=description,
                date=date
            )

        self.accept()

    def populate_data(self):
        """Điền dữ liệu vào các trường trong dialog khi chỉnh sửa giao dịch."""
        self.amount_input.setText(str(self.transaction_data.get("amount", "")))
        self.type_combo.setCurrentText(self.transaction_data.get("transaction_type", "Chi tiêu"))
        self.populate_categories()
        self.category_combo.setCurrentText(self.transaction_data.get("category_name", "Đồ ăn"))
        self.description_input.setText(self.transaction_data.get("description", ""))

        date_str = self.transaction_data.get("date", QDate.currentDate().toString("yyyy-MM-dd"))
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        if date.isValid():
            self.date_edit.setDate(date)

        self.account_combo.setCurrentText(self.transaction_data.get("account_name", "Tiền mặt"))
