from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog

from dialogs import ConfirmDialog, AccountDialog
from widgets import TableWidget, MessageBoxWidget
from datetime import datetime


class AccountScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.message_box = MessageBoxWidget(self)
        self.setContentsMargins(10, 0, 10, 0)
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 1

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.create_header()

        self.column_mapping = {
            0: 'account_name',
            1: 'balance_formated',
            2: 'updated_at',
        }

        self.table_widget = TableWidget(
            main_window=self.main_window,
            current_screen=self,
            page_size=self.page_size,
            edit_dialog=self.open_edit_account_dialog,
            delete_dialog=self.confirm_delete_account,
            column_mapping=self.column_mapping,
        )
        self.layout.addWidget(self.table_widget)

    def initialize(self):
        self.load_total_pages()
        self.load_accounts()

    def create_header(self):
        title = QLabel("Quản Lý Tài Khoản", self)
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
        total_accounts = self.main_window.db_manager.account_manager.count_accounts_for_user(user_id)
        self.total_pages = (total_accounts + self.page_size - 1) // self.page_size

    def load_accounts(self):
        user_id = self.main_window.user_info['user_id']
        offset = self.current_page * self.page_size
        accounts_raw = self.main_window.db_manager.account_manager.get_accounts_for_user(user_id, self.page_size, offset)
        accounts_formatted = self.format_accounts_data(accounts_raw)

        headers = ["Tên Tài Khoản", "Số Dư", "Cập Nhật Lần Cuối"]
        column_widths = [250, 250, 'auto']

        self.table_widget.set_data(headers, accounts_formatted, column_widths)

        self.update_pagination()

    def update_pagination(self):
        current_page_display = self.current_page + 1
        total_pages = self.total_pages

        self.table_widget.update_pagination(current_page_display, total_pages)

    def format_accounts_data(self, accounts_raw):
        formatted_data = []
        for account in accounts_raw:
            account_id = account['account_id']
            account_name = account['account_name']
            balance = account['balance']
            raw_date = account['updated_at']
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

            balance_formatted = f"{balance:,.0f} VND"

            formatted_data.append({
                'account_id': account_id,
                'account_name': account_name,
                'balance': balance,
                'balance_formated': balance_formatted,
                'updated_at': formatted_date,
            })
        return formatted_data

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_accounts()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_accounts()

    def open_edit_account_dialog(self, row):
        account_data = self.table_widget.model._all_data[row]
        dialog = AccountDialog(self.main_window, account_data=account_data)
        dialog.exec_()

    def confirm_delete_account(self, row):
        account_data = self.table_widget.model._all_data[row]
        account_name = account_data['account_name']
        account_id = account_data['account_id']

        dialog = ConfirmDialog(title="Xác nhận xóa", message=f"Bạn có chắc chắn muốn xóa tài khoản '{account_name}'?", parent=self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            try:
                self.main_window.db_manager.account_manager.delete_account(account_id)
                self.load_accounts()
                self.message_box.show_success_message("Tài khoản đã được xóa thành công.")
            except Exception as e:
                self.message_box.show_error_message(f"Đã xảy ra lỗi khi xóa tài khoản: {e}")