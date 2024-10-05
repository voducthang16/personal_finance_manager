from PyQt5.QtWidgets import QWidget
from utils.toast import QToast


class BaseModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

    def toast(self, title, message, toast_type=QToast.SUCCESS, duration=3000):
        QToast(self.parent_window, title, message, duration, toast_type)
