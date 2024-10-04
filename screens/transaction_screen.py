from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class TransactionScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        label = QLabel("Đây là màn hình Giao dich.")
        layout.addWidget(label)

    def initialize(self):
        print("initialize transaction screen")
        print(self.main_window.user_info)