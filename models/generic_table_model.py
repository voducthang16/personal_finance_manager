# models/generic_table_model.py
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class GenericTableModel(QAbstractTableModel):
    def __init__(self, headers=None, data=None, page_size=10):
        super().__init__()
        self.headers = headers or []
        self._all_data = data or []
        self.page_size = page_size
        self.current_page = 0
        self.update_current_page_data()

    def update_current_page_data(self):
        """Cập nhật dữ liệu cho trang hiện tại."""
        start = self.current_page * self.page_size
        end = start + self.page_size
        self._page_data = self._all_data[start:end]

    def rowCount(self, parent=None):
        return len(self._page_data)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return self._page_data[index.row()][index.column()]

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
            else:
                return section + 1
        return QVariant()

    def update_data(self, data):
        """Cập nhật tất cả dữ liệu và reset phân trang."""
        self.beginResetModel()
        self._all_data = data
        self.current_page = 0
        self.update_current_page_data()
        self.endResetModel()

    def next_page(self):
        """Chuyển đến trang kế tiếp."""
        if (self.current_page + 1) * self.page_size < len(self._all_data):
            self.beginResetModel()
            self.current_page += 1
            self.update_current_page_data()
            self.endResetModel()

    def previous_page(self):
        """Chuyển đến trang trước."""
        if self.current_page > 0:
            self.beginResetModel()
            self.current_page -= 1
            self.update_current_page_data()
            self.endResetModel()

    def total_pages(self):
        """Tính tổng số trang."""
        return (len(self._all_data) + self.page_size - 1) // self.page_size
