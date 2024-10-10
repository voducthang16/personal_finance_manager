from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QGridLayout, QWidget, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QDate
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

        # Set default dates to today
        today = QDate.currentDate()
        self.start_date = today
        self.end_date = today

    def initialize(self):
        self.generate_transaction_statistics()
        self.generate_category_statistics()

    def create_header(self):
        # Tạo layout ngang
        layout = QHBoxLayout()

        title = QLabel()
        title.setText("Tổng Quan Tài Chính")
        title.setStyleSheet("""
            font-weight: bold;
            font-size: 24px;
        """)

        # Tạo combo_box và kết nối signal
        self.combo_box = QComboBox()
        self.combo_box.setContentsMargins(0, 0, 0, 0)
        self.combo_box.addItems(["Hôm nay", "Tuần này", "Tháng này", "Quý này"])
        self.setStyleSheet("""
            QComboBox {
                height: 30px;
                max-width: 150px;
                border: 1px solid #292929;
                padding-left: 10px;
                color: #fff;;
                border-radius: 6px;
                font-size: 16px;
            }

            QComboBox::item {
                height: 20px;
                padding: 6px;
                border-radius: 6px;
            }

            QComboBox::item:selected {
                background-color: #3a3a3a;
                color: #fff;
            }

            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 20px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QComboBox::down-arrow {
                image: url('assets/down_arrow.png');
                width: 10px;
                height: 10px;
                margin: 0px;
                padding: 0px;
                alignment: center;
            }
        """)

        self.combo_box.currentIndexChanged.connect(self.handle_selection)

        layout.addWidget(title)
        layout.addWidget(self.combo_box)

        header_widget = QWidget()
        header_widget.setLayout(layout)

        self.layout.addWidget(header_widget)

    def create_overview_finance(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)  # Khoảng cách giữa các ô

        user_id = self.main_window.user_info['user_id']

        # Lấy ngày hiện tại và ngày đầu tháng
        today = QDate.currentDate()
        start_of_month = QDate(today.year(), today.month(), 1).toString("yyyy-MM-dd")
        start_of_last_month = QDate(today.year(), today.month() - 1, 1).toString("yyyy-MM-dd")
        end_of_last_month = QDate(today.year(), today.month() - 1, today.addMonths(-1).daysInMonth()).toString(
            "yyyy-MM-dd")

        # Tổng thu nhập tháng này
        total_income_this_month = self.main_window.db_manager.transaction_manager.get_total_income(user_id, start_of_month, today.toString("yyyy-MM-dd"))
        # Tổng thu nhập tháng trước
        total_income_last_month = self.main_window.db_manager.transaction_manager.get_total_income(user_id, start_of_last_month, end_of_last_month)
        income_note = f"{(total_income_this_month - total_income_last_month) / total_income_last_month * 100:.2f}% so với tháng trước" if total_income_last_month else "N/A"

        # Tổng chi tiêu tháng này
        total_expense_this_month = self.main_window.db_manager.transaction_manager.get_total_expense(user_id, start_of_month, today.toString("yyyy-MM-dd"))
        # Tổng chi tiêu tháng trước
        total_expense_last_month = self.main_window.db_manager.transaction_manager.get_total_expense(user_id, start_of_last_month, end_of_last_month)
        expense_note = f"{(total_expense_this_month - total_expense_last_month) / total_expense_last_month * 100:.2f}% so với tháng trước" if total_expense_last_month else "N/A"

        # Tính toán tiết kiệm (chênh lệch giữa thu nhập và chi tiêu tháng này so với tháng trước)
        savings_this_month = total_income_this_month - total_expense_this_month
        savings_last_month = total_income_last_month - total_expense_last_month
        savings_note = f"{(savings_this_month - savings_last_month) / savings_last_month * 100:.2f}% so với tháng trước" if savings_last_month else "N/A"

        # Số dư hiện tại
        current_balance = self.main_window.db_manager.transaction_manager.get_total_balance(user_id)

        # Tạo dữ liệu hiển thị
        data = [
            {
                "label": "Tổng thu nhập",
                "value": total_income_this_month,
                "note": income_note
            },
            {
                "label": "Tổng chi tiêu",
                "value": total_expense_this_month,
                "note": expense_note
            },
            {
                "label": "Tiết kiệm",
                "value": savings_this_month,
                "note": savings_note
            },
            {
                "label": "Số dư hiện tại",
                "value": current_balance,
                "note": ""
            }
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
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        transactions = self.main_window.db_manager.transaction_manager.get_transactions_by_date_range(user_id, start_date_str, end_date_str)

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
        self.ax.bar(labels, values, color=['#3498db', '#e74c3c', '#2ecc71'])
        self.ax.set_title('Tổng Quan Giao Dịch')
        self.ax.set_xlabel('Loại Giao Dịch')
        self.ax.set_ylabel('Tổng Số Tiền (VND)')

        # Thiết lập ticks và labels
        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels, rotation=45, ha='right')

        self.figure.tight_layout()
        self.canvas.draw()

    def create_category_statistics_widget(self):
        """Tạo widget để hiển thị thống kê danh mục giao dịch."""
        self.figure_cat, self.ax_cat = plt.subplots(figsize=(10, 5))  # Tạo figure cho thống kê danh mục
        self.canvas_cat = FigureCanvas(self.figure_cat)  # Tạo canvas cho figure

    def generate_category_statistics(self):
        """Tạo thống kê danh mục và vẽ biểu đồ pie."""
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        category_stats = self.main_window.db_manager.transaction_manager.get_category_statistics_by_date_range(user_id, start_date_str, end_date_str)

        # Tạo dữ liệu cho biểu đồ
        labels = [category[0] for category in category_stats]
        values = [category[1] for category in category_stats]

        # Xóa biểu đồ cũ
        self.ax_cat.clear()

        # Vẽ biểu đồ pie
        self.ax_cat.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        self.ax_cat.axis('equal')  # Đảm bảo hình tròn

        self.figure_cat.tight_layout()
        self.canvas_cat.draw()

    def handle_selection(self, index):
        current_text = self.combo_box.currentText()

        today = QDate.currentDate()

        if current_text == "Hôm nay":
            self.start_date = today
            self.end_date = today
        elif current_text == "Tuần này":
            self.start_date = today.addDays(-(today.dayOfWeek() - 1))  # Thứ 2
            self.end_date = self.start_date.addDays(6)  # Chủ Nhật
        elif current_text == "Tháng này":
            self.start_date = QDate(today.year(), today.month(), 1)
            self.end_date = QDate(today.year(), today.month(), today.daysInMonth())
        elif current_text == "Quý này":
            current_month = today.month()
            if current_month <= 3:
                start_month = 1
            elif current_month <= 6:
                start_month = 4
            elif current_month <= 9:
                start_month = 7
            else:
                start_month = 10
            self.start_date = QDate(today.year(), start_month, 1)
            self.end_date = QDate(today.year(), start_month + 2, QDate(today.year(), start_month + 2, 1).daysInMonth())

        # Gọi hàm để cập nhật dữ liệu dựa trên khoảng thời gian
        self.generate_transaction_statistics()
        self.generate_category_statistics()
