"""
Add 25,000 more students to the school database.
Run: python add_more_students.py
"""
import pymysql
import random
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'localhost',
    'user': 'onecard_user',
    'password': 'OneCard@2026',
    'database': 'school_test_db',
    'charset': 'utf8mb4'
}

STREAMS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
STUDENTS_PER_STREAM = 520  # ~25,000 total

CLASS_CONFIG = [
    ('Senior 1', 'O', '26', '11', 10000, 700000),
    ('Senior 2', 'O', '25', '12', 20000, 750000),
    ('Senior 3', 'O', '24', '13', 30000, 800000),
    ('Senior 4', 'O', '23', '14', 40000, 850000),
    ('Senior 5', 'A', '22', '15', 50000, 900000),
    ('Senior 6', 'A', '21', '16', 60000, 950000),
]

HOSTEL_STREAMS_OLEVEL = ['C', 'E', 'G', 'H']

MALE_FIRST = [
    'John', 'Peter', 'David', 'Brian', 'Daniel', 'Frank', 'Henry', 'James',
    'Paul', 'Tom', 'Alex', 'Samuel', 'Joseph', 'Michael', 'Andrew', 'Simon',
    'Isaac', 'Moses', 'Robert', 'Charles', 'Mark', 'Stephen', 'Patrick',
    'Geoffrey', 'Ronald', 'Richard', 'William', 'Ben', 'Felix', 'Godfrey',
    'Ivan', 'Kenneth', 'Lawrence', 'Martin', 'Nicholas', 'Oscar', 'Phillip',
    'Raymond', 'Solomon', 'Timothy', 'Vincent', 'Wilson', 'Zachary', 'Emmanuel',
    'Victor', 'Julius', 'Aaron', 'Eric', 'Dennis', 'Calvin', 'Arnold', 'Edwin'
]

FEMALE_FIRST = [
    'Jane', 'Mary', 'Sarah', 'Grace', 'Cathy', 'Esther', 'Gloria', 'Irene',
    'Karen', 'Betty', 'Agnes', 'Diana', 'Faith', 'Hope', 'Mercy', 'Ruth',
    'Joyce', 'Lillian', 'Brenda', 'Susan', 'Alice', 'Rose', 'Florence',
    'Margaret', 'Harriet', 'Sharon', 'Sandra', 'Teddy', 'Annet', 'Prossy',
    'Beatrice', 'Caroline', 'Dorothy', 'Edith', 'Fiona', 'Gladys', 'Hellen',
    'Jackline', 'Lydia', 'Monica', 'Nora', 'Oliver', 'Patricia', 'Martha',
    'Judith', 'Sylvia', 'Barbara', 'Vivian', 'Esther', 'Maureen', 'Rebecca'
]

LAST_NAMES = [
    'Okello', 'Auma', 'Kato', 'Mukasa', 'Nakato', 'Opio', 'Achieng', 'Ssali',
    'Nambi', 'Waiswa', 'Birungi', 'Odongo', 'Adong', 'Opoka', 'Kizza', 'Ocen',
    'Ayo', 'Lwanga', 'Musoke', 'Nabirye', 'Tumusiime', 'Kagwa', 'Kisakye',
    'Mugisha', 'Nakamya', 'Wasswa', 'Babirye', 'Kizito', 'Nanyonjo', 'Ssekandi',
    'Namugga', 'Kiggundu', 'Nantongo', 'Muwanga', 'Lubega', 'Senyonga', 'Kyeyune',
    'Mutyaba', 'Nsubuga', 'Wamala', 'Kibuuka', 'Sserwadda', 'Kawuma', 'Lukwago',
    'Sendagire', 'Kafeero', 'Walusimbi', 'Nakibuuka', 'Kavuma', 'Tamale'
]

PARENT_FIRST = ['JAMES', 'ROBERT', 'FRED', 'PETER', 'DAVID', 'PAUL', 'BRIAN', 'TOM',
                'SARAH', 'GRACE', 'MARY', 'CATHY', 'ESTHER', 'IRENE', 'SHABAN', 'JOHN']
PARENT_LAST = ['OKELLO', 'MUKASA', 'KATO', 'SSALI', 'OPIO', 'ODONGO', 'LWANGA', 'MUSOKE',
               'NAKATO', 'NANKYA', 'BIRUNGI', 'ACHIENG', 'NABIKYE', 'KIZZA', 'NAMBI']

PAYMENT_METHODS = ['MTN_UG', 'MTN_UG', 'MTN_UG', 'Airtel_UG', 'Airtel_UG', 'Bank Transfer', 'Cash']
TERMS = [('Term 1', '2026'), ('Term 2', '2026'), ('Term 3', '2026')]

age_map = {'Senior 1': 14, 'Senior 2': 15, 'Senior 3': 16,
           'Senior 4': 17, 'Senior 5': 18, 'Senior 6': 19}

print("=" * 50)
print("  ADDING 25,000+ STUDENTS")
print("=" * 50)

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

student_count = 0
for class_name, level, year_code, class_code, start_serial, fee in CLASS_CONFIG:
    for stream_idx, stream in enumerate(STREAMS):
        for i in range(STUDENTS_PER_STREAM):
            serial = start_serial + (stream_idx * STUDENTS_PER_STREAM) + i
            admission_number = f"{year_code}-{class_name[-1]}-{serial}"
            payment_code = f"101{class_code}{serial:05d}"

            # Skip if already exists
            cursor.execute("SELECT 1 FROM students WHERE admission_number = %s", [admission_number])
            if cursor.fetchone():
                continue

            is_male = random.random() < 0.48
            first = random.choice(MALE_FIRST if is_male else FEMALE_FIRST)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"
            gender = 'M' if is_male else 'F'

            if level == 'O':
                category = 'hostel' if stream in HOSTEL_STREAMS_OLEVEL else 'day'
            else:
                category = 'hostel' if random.random() < 0.60 else 'day'

            parent_name = f"{random.choice(PARENT_FIRST)} {random.choice(PARENT_LAST)}"
            parent_phone = f"077{random.randint(1000000, 9999999)}"

            age = age_map[class_name]
            dob_year = 2026 - age - random.randint(0, 1)
            dob = f"{dob_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
            admission_date = f"20{year_code}-01-{random.randint(10, 25):02d}"
            status = 'inactive' if random.random() < 0.03 else 'active'

            sql = """INSERT INTO students
                     (admission_number, full_name, current_class, stream, payment_code,
                      category, date_of_birth, gender, parent_name, parent_phone, status, admission_date)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                admission_number, full_name, class_name, stream, payment_code,
                category, dob, gender, parent_name, parent_phone, status, admission_date
            ))
            student_count += 1

            if student_count % 1000 == 0:
                conn.commit()
                print(f"  ✅ {student_count} students added...")

conn.commit()
print(f"\n🎓 TOTAL: {student_count} new students added!")

# Generate payments for new students
print("\n💰 Generating payments for new students...")
cursor.execute("SELECT payment_code, current_class FROM students WHERE status = 'active'")
all_students = cursor.fetchall()

fee_map = {c[0]: c[4] for c in CLASS_CONFIG}
payment_count = 0

for payment_code, class_name in all_students:
    total_fee = fee_map.get(class_name, 800000)
    scenario = random.random()

    if scenario < 0.10:
        continue
    elif scenario < 0.15:
        num_payments = random.randint(1, 3)
        remaining = total_fee + random.randint(50000, 200000)
    elif scenario < 0.75:
        num_payments = random.randint(1, 3)
        remaining = total_fee
    else:
        num_payments = random.randint(1, 2)
        remaining = random.randint(total_fee // 4, total_fee * 3 // 4)

    for t in range(num_payments):
        if t == num_payments - 1:
            amount = remaining
        else:
            amount = random.randint(100000, max(100000, remaining // 2))
            remaining -= amount
        if amount <= 0: continue

        term_info = random.choice(TERMS)
        method = random.choice(PAYMENT_METHODS)
        days_ago = random.randint(1, 160)
        pay_date = datetime.now() - timedelta(days=days_ago)
        trans_id = str(random.randint(100000000, 999999999))

        cursor.execute("""INSERT INTO payments
            (payment_code, amount_paid, payment_date, payment_method, transaction_id, term, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (payment_code, amount, pay_date, method, trans_id, term_info[0], term_info[1]))
        payment_count += 1

conn.commit()
print(f"  💳 {payment_count} payment transactions added!")

# Summary
cursor.execute("SELECT COUNT(*) FROM students")
total = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'active'")
active = cursor.fetchone()[0]
cursor.execute("SELECT category, COUNT(*) FROM students GROUP BY category")
cats = cursor.fetchall()

print("\n" + "=" * 50)
print("  DATABASE SUMMARY")
print("=" * 50)
print(f"  Total Students: {total:,}")
print(f"  Active: {active:,}")
for cat, count in cats:
    print(f"  {cat}: {count:,}")

cursor.close()
conn.close()
print("\n✅ Done!\n")