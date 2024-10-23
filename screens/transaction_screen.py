from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog

from dialogs import TransactionDialog, ConfirmDialog
from widgets import MessageBoxWidget
from widgets.table_widget import TableWidget
from datetime import datetime

class TransactionScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.message_box = MessageBoxWidget(self)
        self.setContentsMargins(10, 0, 10, 0)
        self.page_size = 20
        self.current_page = 0
        self.total_pages = 1

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.create_header()

        self.column_mapping = {
            0: 'account_name',
            1: 'category_name',
            2: 'amount_formatted',
            3: 'transaction_type',
            4: 'date',
            5: 'description',
        }

        self.table_widget = TableWidget(
            main_window=self.main_window,
            current_screen=self,
            page_size=self.page_size,
            edit_dialog=self.open_edit_transaction_dialog,
            delete_dialog=self.confirm_delete_transaction,
            column_mapping=self.column_mapping,
        )
        self.layout.addWidget(self.table_widget)

    def initialize(self):
        self.load_total_pages()
        self.load_transactions()

    def create_header(self):
        title = QLabel("Quản Lý Giao Dịch", self)
        title.setFixedHeight(40)
        title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 24px;
                color: #fff;
            }
        """)
        self.layout.addWidget(title)

    def load_total_pages(self):
        user_id = self.main_window.user_info['user_id']
        total_transactions = len(self.main_window.db_manager.transaction_manager.get_all_transactions(user_id))
        self.total_pages = (total_transactions + self.page_size - 1) // self.page_size

    def load_transactions(self):
        user_id = self.main_window.user_info['user_id']
        offset = self.current_page * self.page_size
        transactions_raw = self.main_window.db_manager.transaction_manager.get_all_transactions(user_id)
        transactions_paginated = transactions_raw[offset: offset + self.page_size]
        transactions_formatted = self.format_transaction_data(transactions_paginated)

        headers = ["Tài Khoản", "Danh Mục", "Số Tiền", "Loại", "Ngày", "Mô Tả"]
        column_widths = [100, 120, 120, 80, 100, 180]

        self.table_widget.set_data(headers, transactions_formatted, column_widths)

        self.update_pagination()

    def update_pagination(self):
        current_page_display = self.current_page + 1
        total_pages = self.total_pages

        self.table_widget.update_pagination(current_page_display, total_pages)

    def format_transaction_data(self, transactions_raw):
        formatted_data = []
        for transaction in transactions_raw:
            transaction_id = transaction['transaction_id']
            account_name = transaction['account_name']
            category_name = transaction['category_name']
            amount = transaction['amount']
            transaction_type = transaction['transaction_type']
            raw_date = transaction['date']
            description = transaction['description']

            amount_formatted = f"{amount:,.0f} VND"
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            formatted_data.append({
                'transaction_id': transaction_id,
                'account_name': account_name,
                'category_name': category_name,
                'amount': amount,
                'amount_formatted': amount_formatted,
                'transaction_type': transaction_type,
                'date': formatted_date,
                'description': description or ""
            })
        return formatted_data

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_transactions()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_transactions()

    def open_edit_transaction_dialog(self, row):
        transaction_data = self.table_widget.model._all_data[row]
        dialog = TransactionDialog(self.main_window, transaction_data=transaction_data)
        dialog.exec_()

    def confirm_delete_transaction(self, row):
        transaction_data = self.table_widget.model._all_data[row]
        transaction_id = transaction_data['transaction_id']
        transaction_description = transaction_data['description']

        dialog = ConfirmDialog(title="Xác nhận xóa", message=f"Bạn có chắc chắn muốn xóa giao dịch '{transaction_description}'?", parent=self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            try:
                self.main_window.db_manager.transaction_manager.delete_transaction(transaction_id)
                self.load_transactions()
                self.message_box.show_success_message("Giao dịch đã được xóa thành công.")
            except Exception as e:
                self.message_box.show_error_message(f"Đã xảy ra lỗi khi xóa giao dịch: {e}")
