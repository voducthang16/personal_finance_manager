import random
import sqlite3
from datetime import datetime, timedelta


# Hàm làm tròn số tiền tới hàng nghìn
def round_amount(amount):
    return round(amount, -3)  # Làm tròn tới hàng nghìn


# Hàm lấy thông tin từ database
def get_user_account_category_data(cursor):
    # Lấy user_id đầu tiên
    cursor.execute("SELECT user_id FROM users LIMIT 1")
    user_id = cursor.fetchone()[0]

    # Lấy danh sách account_id
    cursor.execute("SELECT account_id FROM accounts WHERE user_id = ?", (user_id,))
    account_ids = [row[0] for row in cursor.fetchall()]

    # Lấy danh sách category_id và loại giao dịch tương ứng (Thu nhập hoặc Chi tiêu)
    cursor.execute("SELECT category_id, category_type FROM categories WHERE category_type IN ('Thu nhập', 'Chi tiêu')")
    category_data = cursor.fetchall()

    # Tạo hai danh sách riêng biệt cho thu nhập và chi tiêu
    income_categories = [row[0] for row in category_data if row[1] == 'Thu nhập']
    expense_categories = [row[0] for row in category_data if row[1] == 'Chi tiêu']

    return user_id, account_ids, income_categories, expense_categories


# Hàm để tạo giao dịch ngẫu nhiên
def generate_random_transaction_data(user_id, account_ids, income_categories, expense_categories, start_date, end_date):
    transactions = []
    current_date = start_date

    while current_date <= end_date:
        # Thêm giao dịch thu nhập (lương) vào ngày 1 mỗi tháng
        if current_date.day == 1:
            account_id = random.choice(account_ids)
            category_id = random.choice(income_categories)  # Chọn danh mục thu nhập
            transaction_type = "Thu nhập"
            amount = 15000000  # Lương cố định
            description = f"Lương tháng {current_date.strftime('%m/%Y')}"
            date = current_date.strftime('%Y-%m-%d %H:%M:%S')
            transactions.append((user_id, account_id, category_id, amount, transaction_type, description, date))

        # Thêm giao dịch chi tiêu
        num_transactions = random.randint(2, 3)  # 2-3 giao dịch mỗi ngày
        for _ in range(num_transactions):
            account_id = random.choice(account_ids)
            category_id = random.choice(expense_categories)
            transaction_type = "Chi tiêu"

            # Chọn số tiền dựa trên phân phối xác suất
            rand_percent = random.random()
            if rand_percent < 0.5:
                amount = random.randint(10000, 50000)  # 50% từ 10,000 đến 50,000
            elif rand_percent < 0.8:
                amount = random.randint(50000, 200000)  # 30% từ 50,000 đến 200,000
            else:
                amount = random.randint(200000, 500000)  # 20% từ 200,000 đến 500,000

            # Làm tròn số tiền
            amount = round_amount(amount)

            description = f"Giao dịch {transaction_type} ngày {current_date.strftime('%Y-%m-%d')}"
            date = current_date.strftime('%Y-%m-%d %H:%M:%S')

            transactions.append((user_id, account_id, category_id, amount, transaction_type, description, date))

        # Tăng ngày lên 1
        current_date += timedelta(days=1)

    return transactions


# Ví dụ cách sử dụng:
# Kết nối database và lấy dữ liệu người dùng, tài khoản, danh mục từ database
with sqlite3.connect('personal_finance.db') as conn:
    cursor = conn.cursor()
    user_id, account_ids, income_categories, expense_categories = get_user_account_category_data(cursor)

    # Chọn ngày bắt đầu và kết thúc để sinh giao dịch ngẫu nhiên
    start_date = datetime(2024, 7, 1)
    end_date = datetime(2024, 10, 10)

    # Tạo dữ liệu giao dịch ngẫu nhiên
    transactions = generate_random_transaction_data(user_id, account_ids, income_categories, expense_categories, start_date, end_date)

    # Chèn dữ liệu vào bảng transactions
    try:
        cursor.executemany("""
        INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transactions)
        conn.commit()  # Commit một lần sau khi đã chèn tất cả giao dịch
    except sqlite3.Error as e:
        conn.rollback()  # Rollback nếu có lỗi
        print(f"Lỗi khi thêm giao dịch: {e}")
