"""
Add 1,000 new students to school_test_db with random classes, streams, and payment statuses.
"""
import pymysql
import random
from datetime import datetime, timedelta

conn = pymysql.connect(
    host='localhost', user='onecard_user', password='OneCard@2026',
    database='school_test_db', charset='utf8mb4'
)
cursor = conn.cursor()

# Get max serial numbers per class to continue from
CLASS_SERIAL_MAP = {
    'Senior 1': 1001, 'Senior 2': 2001, 'Senior 3': 3001,
    'Senior 4': 4001, 'Senior 5': 5001, 'Senior 6': 6001,
}

# Find current max serial per class
for class_name in CLASS_SERIAL_MAP:
    year_code = {'Senior 1': '26', 'Senior 2': '25', 'Senior 3': '24',
                 'Senior 4': '23', 'Senior 5': '22', 'Senior 6': '21'}[class_name]
    cursor.execute("""
        SELECT MAX(CAST(SUBSTRING_INDEX(admission_number, '-', -1) AS UNSIGNED))
        FROM students WHERE current_class = %s
    """, [class_name])
    row = cursor.fetchone()
    if row[0]:
        CLASS_SERIAL_MAP[class_name] = row[0] + 1

CLASS_CODES = {
    'Senior 1': ('26', '11'), 'Senior 2': ('25', '12'),
    'Senior 3': ('24', '13'), 'Senior 4': ('23', '14'),
    'Senior 5': ('22', '15'), 'Senior 6': ('21', '16'),
}

STREAMS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
HOSTEL_STREAMS_OLEVEL = ['C', 'E', 'G', 'H']

MALE_FIRST = ['John', 'Peter', 'David', 'Brian', 'Daniel', 'Frank', 'Henry', 'James',
    'Paul', 'Tom', 'Alex', 'Samuel', 'Joseph', 'Michael', 'Andrew', 'Simon',
    'Isaac', 'Moses', 'Robert', 'Charles', 'Mark', 'Stephen', 'Patrick']
FEMALE_FIRST = ['Jane', 'Mary', 'Sarah', 'Grace', 'Cathy', 'Esther', 'Gloria', 'Irene',
    'Karen', 'Betty', 'Agnes', 'Diana', 'Faith', 'Hope', 'Mercy', 'Ruth',
    'Joyce', 'Lillian', 'Brenda', 'Susan', 'Alice', 'Rose', 'Florence']
LAST_NAMES = ['Okello', 'Auma', 'Kato', 'Mukasa', 'Nakato', 'Opio', 'Achieng', 'Ssali',
    'Nambi', 'Waiswa', 'Birungi', 'Odongo', 'Adong', 'Opoka', 'Kizza', 'Ocen',
    'Ayo', 'Lwanga', 'Musoke', 'Nabirye', 'Tumusiime', 'Kagwa', 'Kisakye']

METHODS = ['MTN_UG', 'MTN_UG', 'MTN_UG', 'Airtel_UG', 'Airtel_UG', 'Bank Transfer', 'Cash']

FEE_MAP = {
    ('Senior 1', 'day'): 360000, ('Senior 1', 'hostel'): 670000,
    ('Senior 2', 'day'): 360000, ('Senior 2', 'hostel'): 670000,
    ('Senior 3', 'day'): 360000, ('Senior 3', 'hostel'): 670000,
    ('Senior 4', 'day'): 360000, ('Senior 4', 'hostel'): 670000,
    ('Senior 5', 'day'): 380000, ('Senior 5', 'hostel'): 680000,
    ('Senior 6', 'day'): 380000, ('Senior 6', 'hostel'): 680000,
}

print("Adding 1,000 new students...")
student_count = 0
payment_count = 0

for i in range(1000):
    class_name = random.choice(['Senior 1', 'Senior 2', 'Senior 3', 'Senior 4', 'Senior 5', 'Senior 6'])
    stream = random.choice(STREAMS)
    level = 'O' if class_name in ['Senior 1', 'Senior 2', 'Senior 3', 'Senior 4'] else 'A'
    
    year_code, class_code = CLASS_CODES[class_name]
    serial = CLASS_SERIAL_MAP[class_name]
    CLASS_SERIAL_MAP[class_name] += 1
    
    admission_number = f"{year_code}-{class_name[-1]}-{serial}"
    payment_code = f"101{class_code}{serial:05d}"
    
    is_male = random.random() < 0.48
    first = random.choice(MALE_FIRST if is_male else FEMALE_FIRST)
    last = random.choice(LAST_NAMES)
    full_name = f"{first} {last}"
    gender = 'M' if is_male else 'F'
    
    if level == 'O':
        category = 'hostel' if stream in HOSTEL_STREAMS_OLEVEL else 'day'
    else:
        category = 'hostel' if random.random() < 0.60 else 'day'
    
    dob_year = 2026 - random.randint(14, 20)
    dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    admission_date = f"{year_code}20-01-{random.randint(10,25):02d}"
    parent_phone = f"077{random.randint(1000000, 9999999)}"
    
    cursor.execute("""
        INSERT INTO students (admission_number, full_name, current_class, stream, payment_code,
            category, date_of_birth, gender, parent_name, parent_phone, status, admission_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active', %s)
    """, (admission_number, full_name, class_name, stream, payment_code,
          category, dob, gender, f"Parent of {first}", parent_phone, admission_date))
    student_count += 1
    
    # Generate payment
    total_fee = FEE_MAP.get((class_name, category), 800000)
    scenario = random.random()
    
    if scenario < 0.15:
        pass  # Not paid
    elif scenario < 0.25:
        # Overpaid
        amount = total_fee + random.randint(50000, 200000)
        term = random.choice([('Term 1', '2026'), ('Term 2', '2026')])
        method = random.choice(METHODS)
        days_ago = random.randint(1, 160)
        pay_date = datetime.now() - timedelta(days=days_ago)
        trans_id = str(random.randint(100000000, 999999999))
        cursor.execute("""
            INSERT INTO payments (payment_code, amount_paid, payment_date, payment_method, transaction_id, term, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (payment_code, amount, pay_date, method, trans_id, term[0], term[1]))
        payment_count += 1
    elif scenario < 0.65:
        # Fully paid
        amount = total_fee
        term = random.choice([('Term 1', '2026'), ('Term 2', '2026')])
        method = random.choice(METHODS)
        days_ago = random.randint(1, 160)
        pay_date = datetime.now() - timedelta(days=days_ago)
        trans_id = str(random.randint(100000000, 999999999))
        cursor.execute("""
            INSERT INTO payments (payment_code, amount_paid, payment_date, payment_method, transaction_id, term, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (payment_code, amount, pay_date, method, trans_id, term[0], term[1]))
        payment_count += 1
    else:
        # Partially paid
        amount = random.randint(total_fee // 4, total_fee * 3 // 4)
        term = random.choice([('Term 1', '2026'), ('Term 2', '2026')])
        method = random.choice(METHODS)
        days_ago = random.randint(1, 160)
        pay_date = datetime.now() - timedelta(days=days_ago)
        trans_id = str(random.randint(100000000, 999999999))
        cursor.execute("""
            INSERT INTO payments (payment_code, amount_paid, payment_date, payment_method, transaction_id, term, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (payment_code, amount, pay_date, method, trans_id, term[0], term[1]))
        payment_count += 1
    
    if student_count % 200 == 0:
        conn.commit()
        print(f"  Created {student_count} students...")

conn.commit()

# Show new totals
cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'active'")
total = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM payments")
payments = cursor.fetchone()[0]

print(f"\n=== DONE! ===")
print(f"New students added: {student_count}")
print(f"New payments added: {payment_count}")
print(f"Total active students: {total}")
print(f"Total payments: {payments}")

cursor.close()
conn.close()