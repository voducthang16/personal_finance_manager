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

        background_color = ""
        hover_color = ""
        text_color = "white"

        if icon_type == QMessageBox.Information:
            background_color = '#28a745'
            hover_color = '#218838'
        elif icon_type == QMessageBox.Warning:
            background_color = '#ffc107'
            hover_color = '#e0a800'
            text_color = 'black'
        elif icon_type == QMessageBox.Critical:
            background_color = '#dc3545'
            hover_color = '#c82333'

        style = f"""
            QMessageBox {{
                background-color: #000;
                color: {text_color};
            }}
            QMessageBox QLabel {{
                color: {text_color};
            }}
            QMessageBox QPushButton {{
                background-color: {background_color};
                color: {text_color};
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
        # Get the screen geometry or the parent geometry if available
        if self.parent:
            geometry = self.parent.geometry()
        else:
            screen = QDesktopWidget().availableGeometry()
            geometry = screen

        # Calculate the center position
        center_x = geometry.center().x() - (msg_box.width() // 2)
        center_y = geometry.center().y() - (msg_box.height() // 2)

        # Move the message box to the center
        msg_box.move(center_x, center_y)

    def show_success_message(self, message):
        self.show_message_box("Thành công", message, QMessageBox.Information)

    def show_error_message(self, message):
        self.show_message_box("Lỗi", message, QMessageBox.Critical)

    def show_warning_message(self, message):
        self.show_message_box("Cảnh báo", message, QMessageBox.Warning)