from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from widgets.table_widget import TableWidget

class AccountScreen(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setContentsMargins(10, 0, 10, 0)
        self.page_size = 2  # Số lượng bản ghi trên mỗi trang
        self.current_page = 0  # Bắt đầu từ trang 0
        self.total_pages = 1  # Tổng số trang ban đầu (sẽ tính sau)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.create_header()

        # Table widget to display account information
        self.table_widget = TableWidget(page_size=self.page_size, parent=self)
        self.layout.addWidget(self.table_widget)

    def initialize(self):
        """Tính tổng số trang trước và sau đó tải dữ liệu tài khoản."""
        self.load_total_pages()  # Tính tổng số trang trước
        self.load_accounts()  # Sau đó tải dữ liệu

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
        """Tính tổng số trang dựa trên tổng số tài khoản và kích thước trang."""
        user_id = self.main_window.user_info['user_id']
        total_accounts = self.main_window.db_manager.count_accounts_for_user(user_id)
        self.total_pages = (total_accounts + self.page_size - 1) // self.page_size

    def load_accounts(self):
        """Load account data and populate the table."""
        user_id = self.main_window.user_info['user_id']
        offset = self.current_page * self.page_size  # Tính vị trí bắt đầu của trang hiện tại
        accounts_raw = self.main_window.db_manager.get_accounts_for_user(user_id, self.page_size, offset)
        accounts_formatted = self.format_accounts_data(accounts_raw)

        # Define the headers for the accounts table
        headers = ["Tên Tài Khoản", "Số Dư", "Cập Nhật Lần Cuối"]
        column_widths = [250, 250, 'auto']

        # Pass both headers and formatted accounts data to the table widget
        self.table_widget.set_data(headers, accounts_formatted, column_widths)

        # Cập nhật thông tin phân trang
        self.update_pagination()

    def update_pagination(self):
        """Cập nhật thông tin phân trang cho TableWidget."""
        current_page_display = self.current_page + 1  # Trang bắt đầu từ 1 thay vì 0
        total_pages = self.total_pages

        # Gọi hàm update_pagination của TableWidget và truyền thông tin phân trang
        self.table_widget.update_pagination(current_page_display, total_pages)

    def format_accounts_data(self, accounts_raw):
        """Chuyển đổi dữ liệu thô thành định dạng hiển thị."""
        formatted_data = []
        for account in accounts_raw:
            account_id, user_id, account_name, balance, last_updated = account
            balance_formatted = f"{balance:,.0f} VND"  # Định dạng số dư
            last_updated_formatted = last_updated.split()[0]  # Chỉ lấy ngày
            formatted_data.append([account_name, balance_formatted, last_updated_formatted])
        return formatted_data

    def next_page(self):
        """Chuyển sang trang kế tiếp."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_accounts()

    def previous_page(self):
        """Chuyển về trang trước."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_accounts()
