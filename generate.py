import sqlite3
import random
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

    # Lấy danh sách category_id (chỉ lấy Thu nhập và Chi tiêu)
    cursor.execute("SELECT category_id FROM categories WHERE category_type IN ('Thu nhập', 'Chi tiêu')")
    category_ids = [row[0] for row in cursor.fetchall()]

    return user_id, account_ids, category_ids

# Hàm để tạo giao dịch ngẫu nhiên
def generate_random_transaction_data(user_id, account_ids, category_ids, start_date, end_date):
    transactions = []
    current_date = start_date

    while current_date <= end_date:
        num_transactions = random.randint(2, 3)  # 2-3 giao dịch mỗi ngày
        for _ in range(num_transactions):
            account_id = random.choice(account_ids)
            category_id = random.choice(category_ids)

            # Kiểm tra loại giao dịch dựa trên category_id
            if category_id in [1, 2, 5, 7]:  # Chi tiêu
                transaction_type = "Chi tiêu"
                amount = random.randint(5000, 500000)
            elif category_id in [3, 6]:  # Thu nhập
                transaction_type = "Thu nhập"
                amount = random.randint(5000, 500000)

            # Làm tròn số tiền
            amount = round_amount(amount)

            description = f"Giao dịch {transaction_type} ngày {current_date.strftime('%Y-%m-%d')}"
            date = current_date.strftime('%Y-%m-%d %H:%M:%S')

            transactions.append((user_id, account_id, category_id, amount, transaction_type, description, date))

        # Tăng ngày lên 1
        current_date += timedelta(days=1)

    return transactions


# Kết nối database
conn = sqlite3.connect('personal_finance.db')  # Đường dẫn tới database của bạn
cursor = conn.cursor()

# Lấy thông tin user, account, category từ db
user_id, account_ids, category_ids = get_user_account_category_data(cursor)

# Lấy ngày bắt đầu và kết thúc của quý trước từ bảng transactions
cursor.execute("SELECT MIN(date), MAX(date) FROM transactions WHERE user_id = ?", (user_id,))
start_date_str, end_date_str = cursor.fetchone()
start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S') if start_date_str else datetime(2024, 7, 1)
end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S') if end_date_str else datetime(2024, 10, 10)

# Sinh dữ liệu giao dịch
transactions = generate_random_transaction_data(user_id, account_ids, category_ids, start_date, end_date)

# Chèn dữ liệu vào bảng transactions
for transaction in transactions:
    try:
        cursor.execute("""
        INSERT INTO transactions (user_id, account_id, category_id, amount, transaction_type, description, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, transaction)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm giao dịch: {e}")

# Đóng kết nối
conn.close()
