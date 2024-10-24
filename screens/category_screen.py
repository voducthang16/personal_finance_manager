from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog

from dialogs import ConfirmDialog, CategoryDialog
from widgets import TableWidget, MessageBoxWidget
from datetime import datetime

class CategoryScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.message_box = MessageBoxWidget(self)
        self.setContentsMargins(10, 0, 10, 0)
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 1

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.create_header()

        self.column_mapping = {
            0: 'category_name',
            1: 'category_type',
            2: 'updated_at',
        }

        self.table_widget = TableWidget(
            main_window=self.main_window,
            current_screen=self,
            page_size=self.page_size,
            edit_dialog=self.open_edit_category_dialog,
            delete_dialog=self.confirm_delete_category,
            column_mapping=self.column_mapping,
        )
        self.layout.addWidget(self.table_widget)

    def initialize(self):
        self.load_total_pages()
        self.load_categories()

    def create_header(self):
        title = QLabel("Quản Lý Danh Mục", self)
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
        total_categories = self.main_window.db_manager.category_manager.count_categories()
        self.total_pages = (total_categories + self.page_size - 1) // self.page_size

    def load_categories(self):
        offset = self.current_page * self.page_size
        categories_raw = self.main_window.db_manager.category_manager.get_categories(self.page_size, offset)
        categories_formated = self.format_categories_data(categories_raw)
        headers = ["Tên Danh Mục", "Loại", "Cập Nhật Lần Cuối"]
        column_widths = [150, 150, 150]

        self.table_widget.set_data(headers, categories_formated, column_widths)

        self.update_pagination()

    def format_categories_data(self, categories_raw):
        formatted_data = []
        for category in categories_raw:
            category_id = category['category_id']
            category_name = category['category_name']
            category_type = category['category_type']
            raw_date = category['updated_at']
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

            formatted_data.append({
                'category_id': category_id,
                'category_name': category_name,
                'category_type': category_type,
                'updated_at': formatted_date,
            })
        return formatted_data

    def update_pagination(self):
        current_page_display = self.current_page + 1
        total_pages = self.total_pages

        self.table_widget.update_pagination(current_page_display, total_pages)

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_categories()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_categories()

    def open_edit_category_dialog(self, row):
        category_data = self.table_widget.model._all_data[row]
        dialog = CategoryDialog(self.main_window, category_data=category_data)
        dialog.exec_()

    def confirm_delete_category(self, row):
        category_data = self.table_widget.model._all_data[row]
        category_name = category_data['category_name']
        category_id = category_data['category_id']

        dialog = ConfirmDialog(title="Xác nhận xóa", message=f"Bạn có chắc chắn muốn xóa danh mục '{category_name}'?", parent=self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            try:
                self.main_window.db_manager.category_manager.delete_category(category_id)
                self.load_categories()
                self.message_box.show_success_message("Danh mục đã được xóa thành công")
            except Exception as e:
                self.message_box.show_error_message(f"Đã xảy ra lỗi khi xóa danh mục: {e}")
