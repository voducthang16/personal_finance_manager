from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QWidget, QHBoxLayout, QComboBox, QSizePolicy
from PyQt5.QtCore import Qt, QDate, QDateTime
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DashboardScreen(QWidget):
    def __init__(self, main_window=None):
        super().__init__(main_window)
        self.main_window = main_window

        self.layout = QVBoxLayout(self)

        self.create_header()
        self.create_overview_finance()

        self.create_main_row()
        self.create_total_summary_chart_widget()

        self.layout.addStretch()

        today = QDate.currentDate()
        self.start_date = today
        self.end_date = today

        self.hover_connection = None
        self.initialize()

    def initialize(self):
        self.generate_category_statistics()
        self.generate_total_summary_chart()
        self.update_overview_finance()

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
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)

        data = [
            {
                "label": "Tổng thu nhập",
                "value": 0,
                "note": ""
            },
            {
                "label": "Tổng chi tiêu",
                "value": 0,
                "note": ""
            },
            {
                "label": "Tiết kiệm",
                "value": 0,
                "note": ""
            },
            {
                "label": "Số dư hiện tại",
                "value": 0,
                "note": ""
            }
        ]

        self.overview_labels = {}

        for item in data:
            widget = self.create_item_widget(item)
            label_key = item["label"]
            for child in widget.findChildren(QLabel):
                if child.property("class") == "value":
                    self.overview_labels[label_key + "_value"] = child
                elif child.property("class") == "note":
                    self.overview_labels[label_key + "_note"] = child
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            h_layout.addWidget(widget)

        self.layout.addLayout(h_layout)

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

    def update_overview_finance(self):
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")

        # Xác định loại khoảng thời gian hiện tại
        current_text = self.combo_box.currentText()
        if current_text == "Hôm nay":
            period_type = "hôm"
        elif current_text == "Tuần này":
            period_type = "tuần"
        elif current_text == "Tháng này":
            period_type = "tháng"
        elif current_text == "Quý này":
            period_type = "quý"
        else:
            period_type = "khoảng trước"

        # Tổng thu nhập trong khoảng thời gian hiện tại
        total_income = self.main_window.db_manager.transaction_manager.get_total_income(user_id, start_date_str, end_date_str)

        # Tổng thu nhập trong khoảng thời gian trước đó (để tính % so với trước)
        # Giả sử khoảng thời gian trước đó có độ dài tương tự
        delta_days = self.start_date.daysTo(self.end_date) + 1
        if current_text == "Quý này":
            # Đối với quý, tính khoảng thời gian trước đó là 3 tháng
            prev_start_date = self.start_date.addMonths(-3)
            prev_end_date = self.end_date.addMonths(-3)
        elif current_text == "Tháng này":
            prev_start_date = self.start_date.addMonths(-1)
            prev_end_date = self.end_date.addMonths(-1)
        elif current_text == "Tuần này":
            prev_start_date = self.start_date.addDays(-7)
            prev_end_date = self.end_date.addDays(-7)
        elif current_text == "Hôm nay":
            prev_start_date = self.start_date.addDays(-1)
            prev_end_date = self.end_date.addDays(-1)
        else:
            # Mặc định
            prev_start_date = self.start_date.addDays(-delta_days)
            prev_end_date = self.end_date.addDays(-1)

        prev_start_str = prev_start_date.toString("yyyy-MM-dd")
        prev_end_str = prev_end_date.toString("yyyy-MM-dd")
        total_income_prev = self.main_window.db_manager.transaction_manager.get_total_income(user_id, prev_start_str, prev_end_str)
        if total_income_prev:
            income_change = ((total_income - total_income_prev) / total_income_prev) * 100
            income_note = f"{income_change:.2f}% so với {period_type} trước"
        else:
            income_note = "0% so với " + period_type + " trước"

        # Tổng chi tiêu trong khoảng thời gian hiện tại
        total_expense = self.main_window.db_manager.transaction_manager.get_total_expense(user_id, start_date_str, end_date_str)

        # Tổng chi tiêu trong khoảng thời gian trước đó
        total_expense_prev = self.main_window.db_manager.transaction_manager.get_total_expense(user_id, prev_start_str, prev_end_str)
        if total_expense_prev:
            expense_change = ((total_expense - total_expense_prev) / total_expense_prev) * 100
            expense_note = f"{expense_change:.2f}% so với {period_type} trước"
        else:
            expense_note = "0% so với " + period_type + " trước"

        # Tính toán tiết kiệm
        savings = total_income - total_expense
        savings_prev = total_income_prev - total_expense_prev if total_income_prev and total_expense_prev else 0
        if savings_prev:
            savings_change = ((savings - savings_prev) / savings_prev) * 100
            savings_note = f"{savings_change:.2f}% so với {period_type} trước"
        else:
            savings_note = "0% so với " + period_type + " trước"

        # Số dư hiện tại (có thể không thay đổi dựa trên khoảng thời gian, nhưng nếu cần, có thể tính lại)
        current_balance = self.main_window.db_manager.transaction_manager.get_total_balance(user_id)

        # Cập nhật các QLabel
        self.overview_labels["Tổng thu nhập_value"].setText("{:,.0f} đ".format(total_income))
        self.overview_labels["Tổng thu nhập_note"].setText(income_note)

        self.overview_labels["Tổng chi tiêu_value"].setText("{:,.0f} đ".format(total_expense))
        self.overview_labels["Tổng chi tiêu_note"].setText(expense_note)

        self.overview_labels["Tiết kiệm_value"].setText("{:,.0f} đ".format(savings))
        self.overview_labels["Tiết kiệm_note"].setText(savings_note)

        self.overview_labels["Số dư hiện tại_value"].setText("{:,.0f} đ".format(current_balance))
        self.overview_labels["Số dư hiện tại_note"].setText("")

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
                datetime_obj = QDateTime.fromString(transaction['date'], "yyyy-MM-dd HH:mm:ss")
                date_obj = datetime_obj.date()
                formatted_date = date_obj.toString("dd/MM/yyyy")
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

        self.figure_cat, self.ax_cat = plt.subplots(figsize=(5, 5), dpi=100)

        self.canvas_cat = FigureCanvas(self.figure_cat)

        # Đặt màu nền cho biểu đồ
        self.figure_cat.patch.set_facecolor('#1e1e1e')  # Màu nền của figure
        self.ax_cat.set_facecolor('#1e1e1e')  # Màu nền của axes

        # Bọc canvas trong một QFrame để áp dụng border-radius
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.addWidget(self.canvas_cat)
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
            }
        """)

        layout.addWidget(frame)

    def generate_category_statistics(self):
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")
        category_stats = self.main_window.db_manager.transaction_manager.get_category_statistics_by_date_range(user_id, start_date_str, end_date_str)

        self.ax_cat.clear()

        # Thêm dòng này để điều chỉnh không gian cho biểu đồ và legend
        self.figure_cat.subplots_adjust(left=0.1, right=0.6, top=1.15, bottom=0.0)

        if self.hover_connection is not None:
            self.figure_cat.canvas.mpl_disconnect(self.hover_connection)
            self.hover_connection = None

        if not category_stats:
            self.ax_cat.text(
                0.5, 0.5,
                'Không có dữ liệu để hiển thị',
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.ax_cat.transAxes,
                color='white',
                fontsize=14
            )
            self.ax_cat.set_facecolor('#1e1e1e')
            self.ax_cat.axis('off')
        else:
            labels = [category[0] for category in category_stats]
            values = [category[1] for category in category_stats]

            wedges, texts = self.ax_cat.pie(
                values,
                startangle=90,
                colors=plt.cm.Set3.colors,
                wedgeprops=dict(edgecolor='white')
            )
            self.ax_cat.axis('equal')

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
            plt.setp(legend.get_title(), color='white')

            def on_hover(event):
                if event.inaxes == self.ax_cat:
                    for i, wedge in enumerate(wedges):
                        contains = wedge.contains_point([event.x, event.y])
                        if contains:
                            percentage = values[i] / sum(values) * 100
                            self.ax_cat.set_title(f"{labels[i]}: {percentage:.1f}%", color='white', fontsize=14, y=0.05)
                            self.canvas_cat.draw()
                            break
                    else:
                        self.ax_cat.set_title('')
                        self.canvas_cat.draw()

            self.hover_connection = self.figure_cat.canvas.mpl_connect("motion_notify_event", on_hover)

        self.canvas_cat.draw()

    def create_total_summary_chart_widget(self):
        self.total_summary_chart_widget = QWidget()
        self.total_summary_chart_widget.setContentsMargins(0, 10, 0, 0)

        # Tạo layout chính cho widget
        layout = QVBoxLayout(self.total_summary_chart_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Thêm tiêu đề cho biểu đồ
        title_label = QLabel("Tổng Số Thu Chi Tiêu")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #fff;
        """)
        layout.addWidget(title_label)

        # Tạo figure và canvas cho biểu đồ với figsize phù hợp
        self.figure_total, self.ax_total = plt.subplots(figsize=(10, 4), dpi=100)
        self.canvas_total = FigureCanvas(self.figure_total)

        # Đặt màu nền cho biểu đồ
        self.figure_total.patch.set_facecolor('#1e1e1e')  # Màu nền của figure
        self.ax_total.set_facecolor('#1e1e1e')  # Màu nền của axes

        # Bọc canvas trong một QFrame để áp dụng border-radius
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.addWidget(self.canvas_total)
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
            }
        """)

        self.canvas_total.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(frame, stretch=1)

        self.layout.addWidget(self.total_summary_chart_widget)

    def generate_total_summary_chart(self):
        user_id = self.main_window.user_info['user_id']
        start_date_str = self.start_date.toString("yyyy-MM-dd")
        end_date_str = self.end_date.toString("yyyy-MM-dd")

        # Lấy tổng thu và tổng chi trong khoảng thời gian hiện tại
        total_income = self.main_window.db_manager.transaction_manager.get_total_income(user_id, start_date_str, end_date_str)
        total_expense = self.main_window.db_manager.transaction_manager.get_total_expense(user_id, start_date_str, end_date_str)

        # Xóa biểu đồ cũ
        self.ax_total.clear()

        if total_income == 0 and total_expense == 0:
            # Hiển thị thông báo không có dữ liệu
            self.ax_total.text(0.5, 0.5, 'Không có dữ liệu để hiển thị',
                               horizontalalignment='center',
                               verticalalignment='center',
                               transform=self.ax_total.transAxes,
                               color='white',
                               fontsize=14)
            self.ax_total.set_facecolor('#1e1e1e')
            self.ax_total.axis('off')
        else:
            # Điều chỉnh không gian cho biểu đồ và legend
            self.figure_total.subplots_adjust(left=0.2, right=0.85, top=0.85, bottom=0.15)

            # Tạo dữ liệu cho biểu đồ
            categories = ['Tổng Thu', 'Tổng Chi']
            values = [total_income, total_expense]
            colors = ['#2ecc71', '#e74c3c']  # Màu xanh lá cho thu, màu đỏ cho chi

            # Vẽ biểu đồ cột
            bars = self.ax_total.bar(categories, values, color=colors, width=0.6)

            # Thiết lập giới hạn trục Y để tránh nhãn đụng lên
            max_value = max(values)
            self.ax_total.set_ylim(0, max_value * 1.2)  # Tăng 20% so với giá trị lớn nhất

            # Thêm giá trị trên cột
            for bar in bars:
                height = bar.get_height()
                self.ax_total.text(bar.get_x() + bar.get_width() / 2.0, height,
                                   f"{height:,.0f} đ", ha='center',
                                   va='bottom', color='white', fontsize=12)

            # Đặt tiêu đề và màu sắc
            self.ax_total.set_title("Tổng Thu Chi Tiêu", color='white', fontsize=16)
            self.ax_total.set_facecolor('#1e1e1e')
            self.ax_total.tick_params(axis='y', colors='white')
            self.ax_total.tick_params(axis='x', colors='white')
            self.ax_total.spines['bottom'].set_color('white')
            self.ax_total.spines['left'].set_color('white')
            self.ax_total.spines['right'].set_color('white')
            self.ax_total.spines['top'].set_color('white')

        # Hiển thị biểu đồ
        self.canvas_total.draw()

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

        # Cập nhật phần tổng quan tài chính
        self.update_overview_finance()

        # Cập nhật biểu đồ danh mục khi thay đổi khoảng thời gian
        self.generate_category_statistics()

        self.generate_total_summary_chart()
