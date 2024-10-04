# util/toast.py

from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QFont


class QToast(QLabel):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'

    def __init__(self, message, parent=None, duration=3000, toast_type=SUCCESS):
        super().__init__(parent)
        self.setText(message)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet(self.get_stylesheet(toast_type))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.adjustSize()

        if parent:
            parent_geometry = parent.geometry()
            toast_geometry = self.geometry()
            x = parent_geometry.x() + parent_geometry.width() - toast_geometry.width() - 20  # 20 px margin from the right
            y = parent_geometry.y() + 20  # 20 px margin from the top
            self.move(x, y)
        else:
            # If no parent is provided, center the toast on the screen
            screen_geometry = QApplication.desktop().availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = 20  # 20 px from the top
            self.move(x, y)

        self.setWindowOpacity(0.0)  # Start invisible
        self.show()

        # Fade-in animation
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in.start()

        # Timer for fade-out
        QTimer.singleShot(duration, self.start_fade_out)

    def start_fade_out(self):
        # Fade-out animation
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out.finished.connect(self.close)
        self.fade_out.start()

    def get_stylesheet(self, toast_type):
        """Return the stylesheet based on the toast type."""
        if toast_type == self.SUCCESS:
            background_color = "#28a745"  # Green for success
        elif toast_type == self.ERROR:
            background_color = "#dc3545"  # Red for error
        elif toast_type == self.WARNING:
            background_color = "#ffc107"  # Yellow for warning
        else:
            background_color = "#28a745"  # Default to success

        return f"""
            QLabel {{
                background-color: {background_color};
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
            }}
        """
