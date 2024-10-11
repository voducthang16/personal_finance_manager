from PyQt5.QtWidgets import QMessageBox, QWidget

class MessageBoxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show_message_box(self, title, message, icon_type):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        background_color = ""
        hover_color = ""

        if icon_type == QMessageBox.Information:
            background_color = '#28a745'
            hover_color = '#218838'
        elif icon_type == QMessageBox.Warning:
            background_color = '#ffc107'
            hover_color = '#e0a800'
        elif icon_type == QMessageBox.Critical:
            background_color = '#dc3545'
            hover_color = '#c82333'

        style = f"""
            QPushButton {{
                background-color: {background_color};
                color: white;
                border: none;
                padding: 4px 0px;
                border-radius: 6px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
        msg_box.setStyleSheet(style)
        msg_box.exec_()

    def show_success_message(self, message):
        self.show_message_box("Thành công", message, QMessageBox.Information)

    def show_error_message(self, message):
        self.show_message_box("Lỗi", message, QMessageBox.Critical)

    def show_warning_message(self, message):
        self.show_message_box("Cảnh báo", message, QMessageBox.Warning)
