from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from widgets.scrollabe_widget import ScrollableWidget


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create a widget to hold the rows
        self.rows_container = QWidget(self)  # Ensure rows_container has a parent
        self.rows_layout = QVBoxLayout(self.rows_container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(0)
        self.rows_layout.setAlignment(Qt.AlignTop)

        # Use ScrollableWidget to wrap the rows_container
        self.scrollable_widget = ScrollableWidget(self.rows_container)
        self.main_layout.addWidget(self.scrollable_widget)

        # Initialize header and empty label as None
        self.header = None
        self.empty_label = None

    def initialize(self):
        """Ensure the table and its widgets are properly reinitialized when switching screens."""
        self.clear_rows()

        # Create empty_label if it doesn't exist
        if self.empty_label is None:
            self.empty_label = QLabel("No Data", self.rows_container)
            self.empty_label.setStyleSheet("""
                color: #ffffff;
                margin-top: 10px;
            """)
            self.empty_label.setFont(QFont("Arial", 20))
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.rows_layout.addWidget(self.empty_label)

        self.empty_label.setVisible(False)  # Initially hidden

    def add_header(self, headers):
        """Add a header to the table, removing the old one if it exists."""
        if self.header is not None:
            self.header.deleteLater()  # Remove the old header if it exists

        self.header = QFrame(self)
        self.header.setFixedHeight(50)
        self.header.setStyleSheet("""
            QFrame {
                background-color: #333333;
                border-radius: 0;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QLabel {
                font-weight: bold;
                color: #FFFFFF;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(20)

        # Add dynamic header labels
        for header_text in headers:
            header_label = QLabel(header_text, self)
            header_label.setFont(QFont("Arial", 14))
            header_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            header_layout.addWidget(header_label, alignment=Qt.AlignVCenter)

        self.rows_layout.insertWidget(0, self.header)  # Insert the header at the top

    def add_row(self, columns):
        """Add a dynamic row with the column data."""
        self.empty_label.setVisible(False)  # Hide the empty label if data exists

        row = QFrame(self)
        row.setFixedHeight(40)
        row.setStyleSheet("""
            QFrame {
                background-color: #3c3c3c;
                border-radius: 0;
            }
            QLabel {
                color: #ffffff;
                padding: 10px;
            }
        """)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 0, 10, 0)
        row_layout.setSpacing(20)

        # Add dynamic column labels
        for column_text in columns:
            column_label = QLabel(column_text, self)
            column_label.setFont(QFont("Arial", 13))
            column_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            row_layout.addWidget(column_label, alignment=Qt.AlignVCenter)

        self.rows_layout.addWidget(row)

    def clear_rows(self):
        """Clear all rows, but keep the header and empty label intact."""
        for i in reversed(range(self.rows_layout.count())):
            widget = self.rows_layout.itemAt(i).widget()
            if widget in [self.header, self.empty_label]:
                continue
            self.rows_layout.takeAt(i).widget().deleteLater()

    def set_data(self, headers, data):
        """Populate the table with headers and rows."""
        self.clear_rows()  # Clear previous rows
        if not data:
            self.empty_label.setVisible(True)  # Show the empty label if no data exists
        else:
            self.empty_label.setVisible(False)  # Hide the empty label if data is present
            self.add_header(headers)  # Add the header
            for row_data in data:
                self.add_row(row_data)  # Add the rows
