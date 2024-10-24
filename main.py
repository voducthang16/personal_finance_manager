import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDesktopWidget, QWidget,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QIcon

from constants import SCREEN_NAMES
from database import FinanceManager
from layouts import SetupLayout, LeftMenuWidget
from widgets import ScrollableWidget
from dialogs import AccountDialog, TransactionDialog, CategoryDialog
from screens import DashboardScreen, AccountScreen, SettingScreen, TransactionScreen, CategoryScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
            self.setup_window_property()
            self.show_main_screen()

    def initialize_database(self):
        db_file = 'personal_finance.db'
        if not os.path.exists(db_file):
            print(f"Tạo cơ sở dữ liệu mới: {db_file}")
            self.db_manager = FinanceManager(db_name=db_file)
            self.db_manager.create_tables()
            self.db_manager.set_migration()
        else:
            print(f"Cơ sở dữ liệu đã tồn tại: {db_file}")
            self.db_manager = FinanceManager(db_name=db_file)

    def show_setup_screen(self):
        setup_screen = SetupLayout(main_window=self)
        self.setCentralWidget(setup_screen)

    def show_main_screen(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.left_menu = LeftMenuWidget()

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(10)

        self.top_info_widget = None

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(0, 10, 0, 10)
        self.stacked_widget.setStyleSheet("""
            background-color: #121212;
            border-radius: 10px;
            color: white;
        """)

        self.dashboard_screen = DashboardScreen(main_window=self)
        self.category_screen = CategoryScreen(main_window=self)
        self.transaction_screen = TransactionScreen(main_window=self)
        self.setting_screen = SettingScreen(main_window=self)
        self.account_screen = AccountScreen(main_window=self)

        self.scrollable_dashboard = ScrollableWidget(self.dashboard_screen)

        self.stacked_widget.addWidget(self.scrollable_dashboard)
        self.stacked_widget.addWidget(self.category_screen)
        self.stacked_widget.addWidget(self.transaction_screen)
        self.stacked_widget.addWidget(self.setting_screen)
        self.stacked_widget.addWidget(self.account_screen)

        self.screens = {
            SCREEN_NAMES["DASHBOARD"]: self.scrollable_dashboard,
            SCREEN_NAMES["CATEGORY"]: self.category_screen,
            SCREEN_NAMES["TRANSACTION"]: self.transaction_screen,
            SCREEN_NAMES["ACCOUNT"]: self.account_screen,
            SCREEN_NAMES["SETTING"]: self.setting_screen,
        }

        self.right_layout.addWidget(self.stacked_widget)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)

        main_layout.addWidget(self.left_menu, 1)
        main_layout.addWidget(right_widget, 3)

        self.left_menu.menu_clicked.connect(self.display_screen)

        self.setCentralWidget(main_widget)

        self.display_screen(SCREEN_NAMES["DASHBOARD"])

    def create_top_layout(self, menu_name):
        if self.top_info_widget:
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

        greeting_message = self.get_greeting_message()

        info_label = QLabel(greeting_message)
        info_label.setAlignment(Qt.AlignVCenter)
        info_label.setStyleSheet("font-size: 16px;")

        top_layout.addWidget(info_label)
        top_layout.addStretch()  # push the button to the right

        if menu_name == SCREEN_NAMES["ACCOUNT"]:
            add_account = QPushButton("Thêm Tài Khoản")
            add_account.setFixedSize(160, 40)
            add_account.setStyleSheet("""
                QPushButton {
                    background-color: #e67e22;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #d35400;
                }
            """)
            add_account.clicked.connect(self.open_add_account_dialog)
            top_layout.addWidget(add_account)

        elif menu_name == SCREEN_NAMES["CATEGORY"]:
            add_category = QPushButton("Thêm Danh Mục")
            add_category.setFixedSize(160, 40)
            add_category.setStyleSheet("""
                QPushButton {
                    background-color: #8e44ad;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #71368a;
                }
            """)
            add_category.clicked.connect(self.open_add_category_dialog)
            top_layout.addWidget(add_category)

        elif menu_name == SCREEN_NAMES["TRANSACTION"]:
            add_transaction = QPushButton("Thêm Giao Dịch")
            add_transaction.setFixedSize(160, 40)
            add_transaction.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            add_transaction.clicked.connect(self.open_add_transaction_dialog)
            top_layout.addWidget(add_transaction)

        if self.top_info_widget is not None:
            self.right_layout.insertWidget(0, self.top_info_widget)

    def open_add_category_dialog(self):
        dialog = CategoryDialog(self)
        dialog.exec_()

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
            self.stacked_widget.setCurrentWidget(self.scrollable_dashboard)

    def refresh_current_screen(self):
        current_widget = self.stacked_widget.currentWidget()
        if hasattr(current_widget, 'initialize'):
            current_widget.initialize()

    def setup_window_property(self):
        self.setWindowTitle("Personal Finance Manager")
        self.setWindowIcon(QIcon('assets/logo.png'))

        # set minimum size to 100% width and 100% height of the screen
        screen = QDesktopWidget().availableGeometry()
        min_width = int(screen.width() * 1)
        min_height = int(screen.height() * 1)
        self.setMinimumSize(min_width, min_height)

        # when open app center screen
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

    def get_greeting_message(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()

        if 5 <= hour < 11:
            return "Chào buổi sáng"
        elif 11 <= hour < 13:
            return "Chào buổi trưa"
        elif 13 <= hour < 17:
            return "Chào buổi chiều"
        else:
            return "Chào buổi tối"

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
