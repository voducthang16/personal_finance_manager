from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class TransactionScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("Đây là màn hình Giao dich.")
        layout.addWidget(label)
