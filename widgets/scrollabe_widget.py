from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class ScrollableWidget(QWidget):
    def __init__(self, content_widget):
        super().__init__()
        self.content_widget = content_widget

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.content_widget)

        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setViewportMargins(0, 0, 0, 0)

        scroll_area.setStyleSheet("""
            QScrollArea {
                padding-right: 10px;
                padding-left: 10px;
                border: none;
                background-color: transparent;
            }
        """)

        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def initialize(self):
        if hasattr(self.content_widget, 'initialize'):
            self.content_widget.initialize()