# utils/toast.py

from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


class QToast(QWidget):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'

    def __init__(self, parent, title, message, duration=3000, toast_type=SUCCESS):
        """
        Initialize the QToast.

        :param parent: Parent widget
        :param title: Title of the toast
        :param message: Message body of the toast
        :param duration: Duration in milliseconds
        :param toast_type: Type of toast ('success', 'error', 'warning')
        """
        super().__init__(parent)  # Pass parent to QWidget
        self.title = title
        self.message = message
        self.duration = duration
        self.toast_type = toast_type
        self.setup_ui()
        self.setup_animation()
        self.show_toast()

    def setup_ui(self):
        """
        Set up the UI components of the toast.
        """
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.title_label)

        self.message_label = QLabel(self.message)
        self.message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.get_background_color()};
                border-radius: 8px;
            }}
        """)

        self.adjustSize()
        self.position_toast()

    def get_background_color(self):
        """
        Determine the background color based on the toast type.
        """
        if self.toast_type == self.SUCCESS:
            return "#28a745"  # Green
        elif self.toast_type == self.ERROR:
            return "#dc3545"  # Red
        elif self.toast_type == self.WARNING:
            return "#ffc107"  # Yellow
        else:
            return "#28a745"  # Default to Green

    def position_toast(self):
        """
        Position the toast at the top-right corner of the primary screen.
        """
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 20
        y = 20
        self.move(x, y)

    def setup_animation(self):
        """
        Set up fade-in and fade-out animations for the toast.
        """
        # Fade-in animation
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        # Fade-out animation
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out.finished.connect(self.close)

    def show_toast(self):
        """
        Display the toast with animations.
        """
        self.fade_in.start()
        QTimer.singleShot(self.duration, self.start_fade_out)

    def start_fade_out(self):
        """
        Initiate the fade-out animation.
        """
        self.fade_out.start()
