from PyQt5.QtWidgets import QLineEdit, QComboBox
from dialogs.base_dialog import BaseDialog


class CategoryDialog(BaseDialog):
    def __init__(self, main_window=None, category_data=None):
        self.category_id = category_data['category_id'] if category_data else None
        title = "Sửa Danh Mục" if self.category_id else "Thêm Danh Mục"
        width = 600
        height = 400
        super().__init__(main_window, title=title, width=width, height=height)
        self.main_window = main_window
        self.category_data = category_data
        self.setup_category_fields()
        if self.category_data:
            self.populate_data()

    def setup_category_fields(self):
        # Input cho tên danh mục
        self.category_name_input = QLineEdit()
        self.category_name_input.setFixedHeight(40)
        self.category_name_input.setPlaceholderText("Nhập tên danh mục")
        self.add_content(self.create_row("Tên danh mục:", self.category_name_input))

        # ComboBox cho loại danh mục (Chi tiêu, Thu nhập)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Chi tiêu", "Thu nhập"])
        self.type_combo.setFixedHeight(40)
        self.add_content(self.create_row("Loại danh mục:", self.type_combo))

    def get_category_data(self):
        return {
            "category_name": self.category_name_input.text().strip(),
            "category_type": self.type_combo.currentText(),
        }

    def submit(self):
        try:
            data = self.get_category_data()
            category_name = data["category_name"].strip()
            category_type = data["category_type"]

            if not category_name:
                self.message_box.show_error_message(
                    "Vui lòng nhập tên danh mục hợp lệ (không được để trống hoặc chỉ có khoảng trắng).")
                return

            if self.category_id:
                result = self.main_window.db_manager.category_manager.update_category(self.category_id, category_name, category_type)
            else:
                result = self.main_window.db_manager.category_manager.add_category(category_name, category_type)

            if result is not None:
                self.message_box.show_error_message(result)
            else:
                if self.category_id:
                    self.message_box.show_success_message("Cập nhật danh mục thành công.")
                else:
                    self.message_box.show_success_message("Thêm danh mục thành công.")

                self.main_window.refresh_current_screen()
                self.accept()

        except Exception as e:
            self.message_box.show_error_message(f"Đã xảy ra lỗi: {e}")

    def populate_data(self):
        self.category_name_input.setText(self.category_data.get("category_name", ""))
        
        # Chọn đúng loại danh mục trong ComboBox dựa trên dữ liệu đã lưu
        category_type = self.category_data.get("category_type", "")
        index = self.type_combo.findText(category_type)
        if index != -1:
            self.type_combo.setCurrentIndex(index)
