from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

from constants import SCREEN_NAMES


class LeftMenuWidget(QWidget):
    menu_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_container = QWidget()
        self.menu_container.setObjectName("MenuContainer")

        self.menu_container.setStyleSheet("""
            QWidget#MenuContainer {
                background-color: #121212;
                border-radius: 10px;
            }
            QPushButton {
                padding: 16px;
                font-size: 16px;
                text-align: left;
                border: none;
                border-radius: 8px;
                color: white;
                background-color: transparent;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
                outline: none;
            }
            QPushButton.active {
                background-color: #3e3e3e;
                outline: none;
            }
        """)

        menu_layout = QVBoxLayout(self.menu_container)
        menu_layout.setContentsMargins(10, 10, 10, 10)
        menu_layout.setSpacing(0)

        self.menu_items = [
            SCREEN_NAMES["DASHBOARD"],
            SCREEN_NAMES["CATEGORY"],
            SCREEN_NAMES["TRANSACTION"],
            SCREEN_NAMES["ACCOUNT"],
            SCREEN_NAMES["SETTING"],
        ]
        self.buttons = {}

        for item in self.menu_items:
            button = QPushButton(item)
            button.setCheckable(True)
            button.clicked.connect(self.create_menu_click_handler(item))
            menu_layout.addWidget(button)
            self.buttons[item] = button

        menu_layout.addStretch()

        main_layout.addWidget(self.menu_container)

        self.set_active_button("Tổng Quan")

    def create_menu_click_handler(self, menu_name):
        def handler():
            self.menu_clicked.emit(menu_name)
            self.set_active_button(menu_name)
        return handler

    def set_active_button(self, menu_name):
        for name, button in self.buttons.items():
            if name == menu_name:
                button.setProperty("class", "active")
                button.setChecked(True)
            else:
                button.setProperty("class", "")
                button.setChecked(False)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
