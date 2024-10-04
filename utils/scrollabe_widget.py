from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class ScrollableWidget(QWidget):
    def __init__(self, content_widget):
        super().__init__()
        self.content_widget = content_widget

        # Tạo QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_widget)

        # Loại bỏ viền và thiết lập margin
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setViewportMargins(0, 0, 0, 0)

        # Đặt style sheet cho scroll_area và viewport
        scroll_area.setStyleSheet("""
            QScrollArea {
                padding-right: 10px;
                padding-left: 10px;
                border: none;
                background-color: transparent;
            }
        """)

        # Nếu bạn muốn sử dụng thanh cuộn mặc định, bạn có thể bỏ qua phần này
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Tạo layout cho ScrollableWidget
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def initialize(self):
        if hasattr(self.content_widget, 'initialize'):
            self.content_widget.initialize()