import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDesktopWidget, QWidget,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton
)
from PyQt5.QtCore import Qt

from constants import SCREEN_NAMES
from database import FinanceManager
from layouts import SetupLayout
from widgets import ScrollableWidget
from layouts.left_menu import LeftMenuWidget
from dialogs import AccountDialog, TransactionDialog
from screens import DashboardScreen, AccountScreen, SettingScreen, TransactionScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window_property()

        self.db_manager = None
        self.initialize_database()
        self.user_info = self.get_user_info()

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

        if not self.user_info:
            self.show_setup_screen()
        else:
            self.show_main_screen()

    def initialize_database(self):
        """Hàm kiểm tra và tạo file .db nếu chưa tồn tại."""
        db_file = 'personal_finance.db'
        if not os.path.exists(db_file):
            # Nếu file không tồn tại, tiến hành tạo cơ sở dữ liệu mới
            print(f"Tạo cơ sở dữ liệu mới: {db_file}")
            self.db_manager = FinanceManager(db_name=db_file)
            self.db_manager.create_tables()
        else:
            # Nếu cơ sở dữ liệu đã tồn tại, khởi tạo db_manager
            print(f"Cơ sở dữ liệu đã tồn tại: {db_file}")
            self.db_manager = FinanceManager(db_name=db_file)

    def show_setup_screen(self):
        """Hiển thị màn hình thêm người dùng nếu chưa có người dùng"""
        main_widget = QWidget(self)

        main_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
        """)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        setup_screen = SetupLayout(main_window=self)
        setup_screen_wrapper = QWidget()
        setup_layout = QVBoxLayout(setup_screen_wrapper)
        setup_layout.setContentsMargins(0, 0, 0, 0)
        setup_layout.setAlignment(Qt.AlignCenter)

        setup_screen_wrapper.setStyleSheet("""
            background-color: #1e1e1e;
        """)

        setup_layout.addWidget(setup_screen)

        main_layout.addWidget(setup_screen_wrapper)

        self.setCentralWidget(main_widget)

    def show_main_screen(self):
        """Hiển thị màn hình chính với menu và stacked_widget khi đã có người dùng"""
        # Tạo widget chính và layout chính
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.left_menu = LeftMenuWidget()

        # Tạo layout bên phải với QVBoxLayout
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(10)

        self.top_info_widget = None

        # Tạo stacked_widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 10, 0, 10)  # left, top, right, bottom
        self.stacked_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
            color: white;
        """)

        # init screens
        self.dashboard_screen = DashboardScreen(main_window=self)
        self.transaction_screen = TransactionScreen(main_window=self)
        self.setting_screen = SettingScreen(main_window=self)
        self.account_screen = AccountScreen(main_window=self)

        self.scrollable_dashboard = ScrollableWidget(self.dashboard_screen)
        self.scrollable_transaction = ScrollableWidget(self.transaction_screen)

        self.stacked_widget.addWidget(self.scrollable_dashboard)
        self.stacked_widget.addWidget(self.scrollable_transaction)
        self.stacked_widget.addWidget(self.setting_screen)
        self.stacked_widget.addWidget(self.account_screen)

        # Lưu trữ các màn hình trong từ điển
        self.screens = {
            SCREEN_NAMES["DASHBOARD"]: self.scrollable_dashboard,
            SCREEN_NAMES["TRANSACTION"]: self.scrollable_transaction,
            SCREEN_NAMES["ACCOUNT"]: self.account_screen,
            SCREEN_NAMES["SETTING"]: self.setting_screen,
        }

        # Thêm top_info_widget và stacked_widget vào right_layout
        self.right_layout.addWidget(self.stacked_widget)

        # Tạo một widget để chứa right_layout
        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        # Thêm left_menu và right_widget vào main_layout
        main_layout.addWidget(self.left_menu, 1)
        main_layout.addWidget(right_widget, 3)

        # Kết nối tín hiệu từ menu bên trái
        self.left_menu.menu_clicked.connect(self.display_screen)

        # Đặt main_widget làm central widget
        self.setCentralWidget(main_widget)

        # Hiển thị màn hình mặc định (Trang chủ)
        self.display_screen(SCREEN_NAMES["DASHBOARD"])

    def create_top_layout(self, menu_name):
        if self.top_info_widget:
            # Remove the old widget from the layout if it exists
            self.right_layout.removeWidget(self.top_info_widget)
            self.top_info_widget.deleteLater()

        self.top_info_widget = QWidget()
        self.top_info_widget.setFixedHeight(60)
        self.top_info_widget.setContentsMargins(10, 0, 10, 0)
        self.top_info_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
            color: white;
        """)

        top_layout = QHBoxLayout(self.top_info_widget)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # Label ở bên trái
        info_label = QLabel("Thông tin ở trên cùng")
        info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        info_label.setStyleSheet("font-size: 16px;")

        # Nút ở bên phải
        action_button = QPushButton("Thêm Giao Dịch")
        action_button.setFixedSize(120, 40)
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

        action_button.clicked.connect(self.open_add_transaction_dialog)

        # Thêm widget vào top_layout
        top_layout.addWidget(info_label)
        top_layout.addStretch()  # Đẩy nút về bên phải
        if menu_name == "Tài Khoản":
            add_account = QPushButton("Thêm Tài Khoản")
            add_account.setFixedSize(150, 40)
            add_account.setStyleSheet("""
                QPushButton {
                    background-color: #e67e22;
                    color: white;
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #d35400;
                }
            """)
            add_account.clicked.connect(self.open_add_account_dialog)
            top_layout.addWidget(add_account)
        top_layout.addWidget(action_button)
        if self.top_info_widget is not None:
            self.right_layout.insertWidget(0, self.top_info_widget)

    def open_add_transaction_dialog(self):
        dialog = TransactionDialog(self)
        dialog.exec_()

    def open_add_account_dialog(self):
        dialog = AccountDialog(self)
        dialog.exec_()

    def display_screen(self, menu_name):
        widget = self.screens.get(menu_name)
        if widget:
            self.stacked_widget.setCurrentWidget(widget)
            widget.initialize()
            self.create_top_layout(menu_name)

        else:
            # Nếu không tìm thấy, hiển thị màn hình mặc định
            self.stacked_widget.setCurrentWidget(self.scrollable_dashboard)

    def refresh_current_screen(self):
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'initialize'):
            current_widget.initialize()

    def setup_window_property(self):
        self.setWindowTitle("Personal Finance Manager")

        # Set minimum size to 80% width and 80% height of the screen
        screen = QDesktopWidget().availableGeometry()
        min_width = int(screen.width() * 0.8)
        min_height = int(screen.height() * 0.8)
        self.setMinimumSize(min_width, min_height)

        # Center screen khi mở ứng dụng
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_user_info(self):
        user = self.db_manager.user_manager.get_first_user()
        if not user:
            self.user_info = None
        else:
            self.user_info = user
        return self.user_info

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
