from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QGridLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DashboardScreen(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout(self)

        self.create_header()
        self.create_overview_finance()
        self.create_chart_widget()  # Tạo widget chứa hai biểu đồ

        # Đẩy các widget lên trên
        self.layout.addStretch()

    def initialize(self):
        print("initialize dashboard")
        self.generate_transaction_statistics()
        self.generate_category_statistics()

    def create_header(self):
        title = QLabel()
        title.setText("Tổng Quan Tài Chính")
        title.setStyleSheet("""
            background-color: #292929;
            font-weight: bold;
            font-size: 24px;
        """)
        self.layout.addWidget(title)

    def create_overview_finance(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  # Khoảng cách giữa các ô

        data = [
            {
                "label": "Thu nhập tháng này",
                "value": 15000000,
                "note": "+20% so với tháng trước"
            },
            {
                "label": "Chi phí tháng này",
                "value": 5000000,
                "note": "-10% so với tháng trước"
            },
            {
                "label": "Số khách hàng mới",
                "value": 120,
                "note": "+15% so với tháng trước"
            },
            {
                "label": "Sản phẩm bán ra",
                "value": 300,
                "note": "+5% so với tháng trước"
            },
        ]

        # Duyệt qua dữ liệu và thêm vào lưới
        for index, item in enumerate(data):
            col = index % 4  # Cột hiện tại (0 đến 3)
            row = index // 4  # Hàng hiện tại

            # Tạo widget cho mỗi mục
            widget = self.create_item_widget(item)

            # Thêm widget vào lưới
            grid_layout.addWidget(widget, row, col)

        self.layout.addLayout(grid_layout)

    def create_item_widget(self, item):
        # Tạo khung chứa nội dung
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
                padding: 10px;
            }
            QFrame:hover {
                background-color: #2a2a2a;
            }
            QLabel {
                font-size: 14px;
                background-color: transparent;
            }
            QLabel[class="value"] {
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
            QLabel[class="note"] {
                color: #888888;
                font-size: 12px;
                background-color: transparent;
            }
        """)

        # Tạo layout cho khung
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tạo label cho "label"
        label = QLabel(item["label"])
        label.setAlignment(Qt.AlignLeft)

        # Tạo label cho "value"
        value_text = "{:,.0f} đ".format(item["value"])
        value = QLabel(value_text)
        value.setAlignment(Qt.AlignLeft)
        value.setProperty("class", "value")

        # Tạo label cho "note"
        note = QLabel(item["note"])
        note.setAlignment(Qt.AlignLeft)
        note.setProperty("class", "note")

        # Thêm các label vào layout
        layout.addWidget(label)
        layout.addWidget(value)
        layout.addWidget(note)

        return frame

    def create_chart_widget(self):
        """Tạo widget chứa hai biểu đồ."""
        chart_widget = QWidget()
        chart_layout = QHBoxLayout(chart_widget)

        # Biểu đồ thống kê giao dịch
        self.create_transaction_statistics_widget()
        chart_layout.addWidget(self.canvas, stretch=6)  # Chiếm 60% chiều rộng

        # Biểu đồ thống kê danh mục
        self.create_category_statistics_widget()
        chart_layout.addWidget(self.canvas_cat, stretch=4)  # Chiếm 40% chiều rộng

        self.layout.addWidget(chart_widget)

    def create_transaction_statistics_widget(self):
        """Tạo widget để hiển thị thống kê giao dịch."""
        self.figure, self.ax = plt.subplots(figsize=(10, 5))  # Tạo figure
        self.canvas = FigureCanvas(self.figure)  # Tạo canvas cho figure

    def generate_transaction_statistics(self):
        """Tạo thống kê giao dịch và vẽ biểu đồ."""
        user_id = self.main_window.user_info['user_id']  # Lấy user_id từ thông tin người dùng
        transactions = self.main_window.db_manager.transaction_manager.get_transactions_from_start_of_october(user_id)

        # Tính tổng số tiền theo loại giao dịch
        transaction_stats = defaultdict(float)
        for transaction in transactions:
            amount = transaction[4]  # amount
            transaction_type = transaction[5]  # transaction_type
            transaction_stats[transaction_type] += amount

        # Tạo dữ liệu cho biểu đồ
        labels = list(transaction_stats.keys())
        values = list(transaction_stats.values())

        # Xóa biểu đồ cũ
        self.ax.clear()

        # Vẽ biểu đồ
        self.ax.bar(labels, values, color=['#3498db', '#e74c3c', '#2ecc71'])  # Màu cho từng loại giao dịch
        self.ax.set_title('Tổng Quan Giao Dịch Từ Đầu Tháng 10')
        self.ax.set_xlabel('Loại Giao Dịch')
        self.ax.set_ylabel('Tổng Số Tiền (VND)')

        # Thiết lập ticks và labels
        self.ax.set_xticks(range(len(labels)))  # Đặt ticks cho từng label
        self.ax.set_xticklabels(labels, rotation=45, ha='right')  # Căn chỉnh nhãn cho dễ đọc

        self.figure.tight_layout()
        self.canvas.draw()  # Vẽ lại canvas

    def create_category_statistics_widget(self):
        """Tạo widget để hiển thị thống kê danh mục giao dịch."""
        self.figure_cat, self.ax_cat = plt.subplots(figsize=(10, 5))  # Tạo figure cho thống kê danh mục
        self.canvas_cat = FigureCanvas(self.figure_cat)  # Tạo canvas cho figure

    def generate_category_statistics(self):
        """Tạo thống kê danh mục và vẽ biểu đồ pie."""
        user_id = self.main_window.user_info['user_id']  # Lấy user_id từ thông tin người dùng
        category_stats = self.main_window.db_manager.transaction_manager.get_category_statistics_from_start_of_october(user_id)

        # Tạo dữ liệu cho biểu đồ
        labels = [category[0] for category in category_stats]  # Tên danh mục
        values = [category[1] for category in category_stats]  # Tổng số tiền theo danh mục

        # Xóa biểu đồ cũ
        self.ax_cat.clear()

        # Vẽ biểu đồ pie
        self.ax_cat.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        self.ax_cat.axis('equal')  # Đảm bảo hình tròn

        self.figure_cat.tight_layout()
        self.canvas_cat.draw()  # Vẽ lại canvas
