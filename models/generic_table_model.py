from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class GenericTableModel(QAbstractTableModel):
    def __init__(self, headers=None, data=None, page_size=10, column_mapping=None):
        super().__init__()
        self.headers = headers or []
        self._all_data = data or []
        self.page_size = page_size
        self.column_mapping = column_mapping or {}
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
        # Thêm một cột cho Action (Edit/Delete)
        return len(self.headers) + 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            if index.column() < len(self.headers):
                # return value with mapping column
                return self._page_data[index.row()].get(self.column_mapping.get(index.column(), ""), "")
            else:
                return ""

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "Action"
            else:
                return section + 1
        return QVariant()

    def update_data(self, data):
        self.beginResetModel()
        self._all_data = data
        self.current_page = 0
        self.update_current_page_data()
        self.endResetModel()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self._all_data):
            self.beginResetModel()
            self.current_page += 1
            self.update_current_page_data()
            self.endResetModel()

    def previous_page(self):
        if self.current_page > 0:
            self.beginResetModel()
            self.current_page -= 1
            self.update_current_page_data()
            self.endResetModel()

    def total_pages(self):
        return (len(self._all_data) + self.page_size - 1) // self.page_size
