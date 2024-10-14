from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QGridLayout, QWidget, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QDate, QDateTime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

class DashboardScreen(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout(self)

        self.create_header()
        self.create_overview_finance()

        # Tạo một hàng chứa recent_transactions_widget và chart
        self.create_main_row()

        self.layout.addStretch()

        today = QDate.currentDate()
        self.start_date = today
        self.end_date = today

        self.initialize()

    def initialize(self):
        # Khởi tạo biểu đồ danh mục
        self.generate_category_statistics()

    def create_header(self):
        layout = QHBoxLayout()

        title = QLabel()
        title.setText("Tổng Quan Tài Chính")
        title.setStyleSheet("""
            font-weight: bold;
            font-size: 24px;
        """)

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
        grid_layout.setSpacing(10)

        user_id = self.main_window.user_info['user_id']

        today = QDate.currentDate()
        start_of_month = QDate(today.year(), today.month(), 1).toString("yyyy-MM-dd")
        start_of_last_month = QDate(today.year(), today.month() - 1, 1).toString("yyyy-MM-dd")
        end_of_last_month = QDate(today.year(), today.month() - 1, today.addMonths(-1).daysInMonth()).toString("yyyy-MM-dd")

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

        for index, item in enumerate(data):
            col = index % 4
            row = index // 4

            widget = self.create_item_widget(item)

            grid_layout.addWidget(widget, row, col)

        self.layout.addLayout(grid_layout)

    def create_item_widget(self, item):
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

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(item["label"])
        label.setAlignment(Qt.AlignLeft)

        value_text = "{:,.0f} đ".format(item["value"])
        value = QLabel(value_text)
        value.setAlignment(Qt.AlignLeft)
        value.setProperty("class", "value")

        note = QLabel(item["note"])
        note.setAlignment(Qt.AlignLeft)
        note.setProperty("class", "note")

        layout.addWidget(label)
        layout.addWidget(value)
        layout.addWidget(note)

        return frame

    def create_main_row(self):
        main_row_widget = QWidget()
        main_row_layout = QHBoxLayout(main_row_widget)
        main_row_layout.setContentsMargins(0, 10, 0, 0)

        self.create_recent_transactions_widget()
        self.create_category_statistics_widget()

        main_row_layout.addWidget(self.recent_transactions_widget, stretch=1)
        main_row_layout.addWidget(self.category_statistics_widget, stretch=1)

        self.layout.addWidget(main_row_widget)

    def create_recent_transactions_widget(self):
        self.recent_transactions_widget = QWidget()
        layout = QVBoxLayout(self.recent_transactions_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        title_label = QLabel("Giao dịch gần nhất")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #fff;
        """)
        layout.addWidget(title_label)

        user_id = self.main_window.user_info['user_id']
        transactions = self.main_window.db_manager.transaction_manager.get_all_transactions(user_id, limit=5)
        if not transactions:
            no_data_label = QLabel("Không có giao dịch nào")
            no_data_label.setStyleSheet("font-size: 14px; color: #888888;")
            layout.addWidget(no_data_label)
        else:
            for transaction in transactions:
                transaction_widget = QFrame()
                transaction_layout = QHBoxLayout(transaction_widget)
                transaction_layout.setSpacing(10)

                left_layout = QVBoxLayout()
                category_label = QLabel(transaction['category_name'])
                category_label.setStyleSheet("font-size: 14px; color: #fff;")
                raw_date = transaction['date']
                formatted_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
                QDateTime.fromString(transaction['date'], "yyyy-MM-dd HH:mm:ss")
                date_label = QLabel(formatted_date)
                date_label.setStyleSheet("font-size: 12px; color: #888888;")
                left_layout.addWidget(category_label)
                left_layout.addWidget(date_label)
                left_layout.addStretch()

                amount_label = QLabel(f"{transaction['amount']:,} đ")
                amount_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                amount_label.setStyleSheet("""
                    font-size: 16px;
                    font-weight: bold;
                    color: #e74c3c;
                """)

                if transaction['transaction_type'] == 'Income':
                    amount_label.setStyleSheet("""
                        font-size: 16px;
                        font-weight: bold;
                        color: #2ecc71;
                    """)

                transaction_layout.addLayout(left_layout)
                transaction_layout.addWidget(amount_label)

                transaction_widget.setLayout(transaction_layout)

                transaction_widget.setStyleSheet("""
                    QFrame {
                        background-color: #1e1e1e;
                        border-radius: 8px;
                    }
                """)

                layout.addWidget(transaction_widget)

        layout.addStretch()

    def create_category_statistics_widget(self):
        """Tạo widget cho biểu đồ danh mục"""
        self.category_statistics_widget = QWidget()
        layout = QVBoxLayout(self.category_statistics_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Thêm tiêu đề cho biểu đồ
        title_label = QLabel("Thống kê danh mục")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #fff;
        """)
        layout.addWidget(title_label)

        # Tạo figure và canvas cho biểu đồ
        self.figure_cat, self.ax_cat = plt.subplots(figsize=(5, 5))
        self.canvas_cat = FigureCanvas(self.figure_cat)

        # Đặt màu nền cho biểu đồ
        self.figure_cat.patch.set_facecolor('#1e1e1e')  # Màu nền của figure
        self.ax_cat.set_facecolor('#1e1e1e')  # Màu nền của axes

        # Bọc canvas trong một QFrame để áp dụng border-radius
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.canvas_cat)
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
            }
        """)

        layout.addWidget(frame)

    def generate_category_statistics(self):
        """Hàm vẽ biểu đồ danh mục"""
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        category_stats = self.main_window.db_manager.transaction_manager.get_category_statistics_by_date_range(user_id, start_date_str, end_date_str)

        # Xóa biểu đồ cũ
        self.ax_cat.clear()

        if not category_stats:
            # Nếu không có dữ liệu, hiển thị thông báo
            self.ax_cat.text(0.5, 0.5, 'Không có dữ liệu để hiển thị', horizontalalignment='center',
                             verticalalignment='center', transform=self.ax_cat.transAxes, color='white', fontsize=14)
            self.ax_cat.set_facecolor('#1e1e1e')  # Màu nền của axes
            self.ax_cat.axis('off')  # Tắt các trục
        else:
            # Tạo dữ liệu cho biểu đồ
            labels = [category[0] for category in category_stats]
            values = [category[1] for category in category_stats]

            # Vẽ biểu đồ pie mà không hiển thị labels và percentages trên các phần
            wedges = self.ax_cat.pie(
                values,
                startangle=90,
                colors=plt.cm.Set3.colors  # Sử dụng bảng màu
            )[0]
            self.ax_cat.axis('equal')  # Đảm bảo hình tròn

            # Thêm border màu trắng cho các phần của biểu đồ
            for wedge in wedges:
                wedge.set_edgecolor('white')

            # Cập nhật legend với labels màu trắng
            legend = self.ax_cat.legend(
                wedges,
                labels,
                title="Danh mục",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                facecolor='#1e1e1e',
                edgecolor='#1e1e1e',
                labelcolor='white'
            )
            # Đặt màu cho tiêu đề của legend
            plt.setp(legend.get_title(), color='white')

            # Thêm sự kiện hover để hiển thị phần trăm
            def on_hover(event):
                # Kiểm tra nếu con trỏ chuột nằm trong vùng biểu đồ
                if event.inaxes == self.ax_cat:
                    for i, wedge in enumerate(wedges):
                        if wedge.contains_point([event.x, event.y]):
                            percentage = values[i] / sum(values) * 100
                            self.ax_cat.set_title(f"{labels[i]}: {percentage:.1f}%", color='white', fontsize=14, y=0.1)
                            self.canvas_cat.draw()
                            break
                    else:
                        self.ax_cat.set_title('')
                        self.canvas_cat.draw()

            self.figure_cat.canvas.mpl_connect("motion_notify_event", on_hover)

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
            end_month = start_month + 2
            end_day = QDate(today.year(), end_month, 1).daysInMonth()
            self.end_date = QDate(today.year(), end_month, end_day)

        # Cập nhật biểu đồ danh mục khi thay đổi khoảng thời gian
        self.generate_category_statistics()
