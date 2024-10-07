from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QLabel, QHBoxLayout, QHeaderView
from models.generic_table_model import GenericTableModel

class TableWidget(QWidget):
    def __init__(self, parent=None, page_size=10):
        super().__init__(parent)
        self.page_size = page_size

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # QTableView
        self.table_view = QTableView()
        self.model = GenericTableModel(page_size=self.page_size)
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setAlternatingRowColors(True)

        # Custom style for QTableView
        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #1d1f21;  /* Nền màu đen nhạt */
                color: #c5c8c6;  /* Màu chữ xám nhạt */
                gridline-color: #282a2e;  /* Màu đường kẻ */
                border: 1px solid #373b41;  /* Đường viền màu xám đậm */
                font-size: 14px;  /* Kích thước chữ */
            }
            QHeaderView::section {
                background-color: #282a2e;  /* Nền tiêu đề */
                color: #ffffff;  /* Màu chữ tiêu đề */
                padding: 4px;  /* Khoảng cách trong tiêu đề */
                border: none;  /* Bỏ viền */
                font-weight: bold;  /* Chữ đậm cho tiêu đề */
            }
            QHeaderView::section:first {
                border-top-left-radius: 10px;  /* Bo góc trái trên cùng */
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;  /* Bo góc phải trên cùng */
            }
            QTableView::item {
                padding: 10px;  /* Khoảng cách giữa các mục */
            }
            QTableView::item:selected {
                background-color: #373b41;  /* Màu nền khi được chọn */
                color: #ffffff;  /* Màu chữ khi được chọn */
            }
            QScrollBar:vertical {
                background-color: #282a2e;  /* Nền thanh cuộn */
                width: 12px;  /* Độ rộng thanh cuộn */
            }
            QScrollBar::handle:vertical {
                background-color: #373b41;  /* Màu thanh kéo */
                min-height: 20px;  /* Chiều cao tối thiểu */
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4e5358;  /* Màu thanh kéo khi hover */
            }
        """)

        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table_view)

        # Pagination controls
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Trang Trước")
        self.next_button = QPushButton("Trang Tiếp")
        self.page_label = QLabel("Trang 1 / 1")

        # Kết nối sự kiện nút
        self.prev_button.clicked.connect(parent.previous_page)  # Kết nối tới AccountScreen
        self.next_button.clicked.connect(parent.next_page)  # Kết nối tới AccountScreen

        # Thiết lập styles cho nút
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)

        # Thêm các widget vào layout phân trang
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.next_button)

        self.layout.addLayout(self.pagination_layout)

    def set_data(self, headers, data, column_widths=None):
        """Thiết lập dữ liệu cho bảng."""
        self.model.headers = headers
        self.model.update_data(data)

        if column_widths:
            for i, width in enumerate(column_widths):
                if i < len(headers):
                    if width == 'auto':
                        self.table_view.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)  # Auto width
                    elif width == 'stretch':
                        self.table_view.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)  # Flexible width
                    else:
                        self.table_view.setColumnWidth(i, width)  # Fixed width

    def update_pagination(self, current_page, total_pages):
        """Cập nhật thông tin phân trang dựa trên dữ liệu từ AccountScreen."""
        self.page_label.setText(f"Trang {current_page} / {total_pages}")

        # Cập nhật trạng thái của nút phân trang
        self.prev_button.setEnabled(current_page > 1)
        self.next_button.setEnabled(current_page < total_pages)
