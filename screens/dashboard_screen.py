import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt


class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.create_header()
        self.create_overview_finance()

        # Đẩy các widget lên trên
        self.layout.addStretch()

    def create_header(self):
        title = QLabel()
        title.setText("Tổng Quan Tài Chính")
        title.setStyleSheet("""
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
