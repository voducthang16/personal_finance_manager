from PyQt5.QtWidgets import QMessageBox, QWidget, QDesktopWidget


class MessageBoxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def show_message_box(self, title, message, icon_type):
        msg_box = QMessageBox(self.parent)
        msg_box.setFixedSize(400, 250)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)

        if icon_type == QMessageBox.Information:
            hover_color = '#218838'
            button_color = '#28a745'
        elif icon_type == QMessageBox.Warning:
            hover_color = '#e0a800'
            button_color = '#ffc107'
        elif icon_type == QMessageBox.Critical:
            hover_color = '#c82333'
            button_color = '#dc3545'
        else:
            button_color = '#5dade2'
            hover_color = '#3498db'

        style = f"""
            QMessageBox#customMessageBox {{
                background-color: #000;
                color: #fff;
            }}
            QMessageBox QLabel {{
                color: #fff;
            }}
            QMessageBox QPushButton {{
                background-color: {button_color};
                color: #fff;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                min-width: 80px;
                font-size: 14px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {hover_color};
            }}
            QMessageBox QLabel {{
                min-width: 240px;
                min-height: 50px;
            }}
        """
        msg_box.setStyleSheet(style)

        self.center_on_screen(msg_box)

        msg_box.exec_()

    def center_on_screen(self, msg_box):
        screen = QDesktopWidget().availableGeometry()
        geometry = screen

        center_x = geometry.center().x() - (msg_box.width() // 2)
        center_y = geometry.center().y() - (msg_box.height() // 2)

        msg_box.move(center_x, center_y)

    def show_success_message(self, message):
        self.show_message_box("Thành công", message, QMessageBox.Information)

    def show_error_message(self, message):
        self.show_message_box("Lỗi", message, QMessageBox.Critical)

    def show_warning_message(self, message):
        self.show_message_box("Cảnh báo", message, QMessageBox.Warning)