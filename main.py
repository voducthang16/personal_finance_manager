import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDesktopWidget, QWidget,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QDialog
)
from PyQt5.QtCore import Qt

from left_menu import LeftMenuWidget
from screens.dashboard_screen import DashboardScreen
from screens.transaction import TransactionScreen
from utils.scrollabe_widget import ScrollableWidget
from transaction_dialog import TransactionDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window_property()
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("""
            QScrollBar {
                background: red;
                width: 8px;
                margin: 0px;
                padding: 0px;
            }
            QScrollBar::handle {
                background: rgba(125, 125, 125, 50);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:hover {
                background: rgba(125, 125, 125, 200);
            }
            QScrollBar::add-line,
            QScrollBar::sub-line {
                height: 0px;
                width: 0px;
            }
            QScrollBar::add-page,
            QScrollBar::sub-page {
                background: none;
            }
            QWidget {
                background-color: #000;
            }
        """)

        # Tạo widget chính và layout chính
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.left_menu = LeftMenuWidget()

        # Tạo layout bên phải với QVBoxLayout
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Tạo widget thông tin ở trên cùng
        top_info_widget = QWidget()
        top_info_widget.setFixedHeight(60)
        top_info_widget.setContentsMargins(10, 0, 10, 0)
        top_info_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
            color: white;
        """)

        top_layout = QHBoxLayout(top_info_widget)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Label ở bên trái
        info_label = QLabel("Thông tin ở trên cùng")
        info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        info_label.setStyleSheet("font-size: 16px;")

        # Nút ở bên phải
        action_button = QPushButton("Mở Modal")
        action_button.setFixedSize(100, 40)
        action_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Kết nối nút với hàm mở modal
        action_button.clicked.connect(self.open_add_transaction_dialog)

        # Thêm widget vào top_layout
        top_layout.addWidget(info_label)
        top_layout.addStretch()  # Đẩy nút về bên phải
        top_layout.addWidget(action_button)

        # Tạo stacked_widget như trước
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 10, 0, 10)  # left, top, right, bottom
        self.stacked_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
            color: white;
        """)

        self.dashboard_screen = DashboardScreen()
        self.transaction_screen = TransactionScreen()

        self.scrollable_dashboard = ScrollableWidget(self.dashboard_screen)
        self.scrollable_transaction = ScrollableWidget(self.transaction_screen)

        self.stacked_widget.addWidget(self.scrollable_dashboard)
        self.stacked_widget.addWidget(self.scrollable_transaction)

        # Lưu trữ các màn hình trong từ điển
        self.screens = {
            "Tổng Quan": self.scrollable_dashboard,
            "Giao Dịch": self.scrollable_transaction,
            # "Liên hệ": self.contact_screen,  # Nếu không cần cuộn
        }

        # Thêm top_info_widget và stacked_widget vào right_layout
        right_layout.addWidget(top_info_widget)
        right_layout.addWidget(self.stacked_widget)

        # Tạo một widget để chứa right_layout
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # Thêm left_menu và right_widget vào main_layout
        main_layout.addWidget(self.left_menu, 1)
        main_layout.addWidget(right_widget, 3)

        # Kết nối tín hiệu từ menu bên trái
        self.left_menu.menu_clicked.connect(self.display_screen)

        # Đặt main_widget làm central widget
        self.setCentralWidget(main_widget)

        # Hiển thị màn hình mặc định (Trang chủ)
        self.display_screen("Tổng Quan")

    def open_add_transaction_dialog(self):
        dialog = TransactionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_transaction_data()
            # Xử lý dữ liệu giao dịch mới (ví dụ: thêm vào cơ sở dữ liệu hoặc cập nhật giao diện)
            print("Giao dịch mới:", data)

    def display_screen(self, menu_name):
        widget = self.screens.get(menu_name)
        if widget:
            self.stacked_widget.setCurrentWidget(widget)
        else:
            # Nếu không tìm thấy, hiển thị màn hình mặc định
            self.stacked_widget.setCurrentWidget(self.scrollable_dashboard)

    def setup_window_property(self):
        self.setWindowTitle("Personal Finance Manager")

        # Set minimum size to 80% width and 80% height of the screen
        screen = QDesktopWidget().availableGeometry()
        min_width = int(screen.width() * 0.8)
        min_height = int(screen.height() * 0.8)
        self.setMinimumSize(min_width, min_height)

        # Center screen khi mở ứng dụng
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
