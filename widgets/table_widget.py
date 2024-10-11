from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView, QHBoxLayout
from PyQt5.QtWidgets import QPushButton

from models import GenericTableModel
from widgets.action_widget import ActionWidget

class TableWidget(QWidget):
    def __init__(self, main_window=None, current_screen=None, page_size=10, edit_dialog=None, delete_dialog=None, column_mapping=None):
        super().__init__(current_screen)
        self.main_window = main_window
        self.current_screen = current_screen
        self.page_size = page_size
        self.edit_dialog = edit_dialog
        self.delete_dialog = delete_dialog
        self.column_mapping = column_mapping

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # QTableView
        self.table_view = QTableView()
        self.model = GenericTableModel(page_size=self.page_size, column_mapping=self.column_mapping)
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
            /* Tùy chỉnh border-radius cho mục đầu tiên và cuối cùng */
            QHeaderView::section:first {
                border-top-left-radius: 10px;  /* Bo góc trái trên cùng */
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;  /* Bo góc phải trên cùng */
            }
            QTableView::item {
                padding: 0px;  /* Reset padding for items */
                margin: 0px;   /* Reset margin for items */
                background-color: #1d1f21;
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
        self.prev_button.clicked.connect(self.current_screen.previous_page)
        self.next_button.clicked.connect(self.current_screen.next_page)

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

        for row in range(self.model.rowCount()):
            action_widget = ActionWidget(
                parent=self.table_view,
                edit_callback=self.edit_dialog,
                delete_callback=self.delete_dialog,
                row=row,
            )
            self.table_view.setRowHeight(row, 40)
            self.table_view.setIndexWidget(self.model.index(row, len(headers)), action_widget)

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
        self.page_label.setText(f"Trang {current_page} / {total_pages}")

        # Cập nhật trạng thái của nút phân trang
        self.prev_button.setEnabled(current_page > 1)
        self.next_button.setEnabled(current_page < total_pages)
