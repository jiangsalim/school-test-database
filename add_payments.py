"""
Add more payment transactions to create a realistic mix:
- 40% Fully Cleared
- 35% Partially Paid (Not Cleared)
- 15% Not Paid at All
- 10% Overpaid
"""
import pymysql
import random
from datetime import datetime, timedelta

conn = pymysql.connect(
    host='localhost', user='onecard_user', password='OneCard@2026',
    database='school_test_db', charset='utf8mb4'
)
cursor = conn.cursor()

FEE_MAP = {
    ('Senior 1', 'day'): 360000, ('Senior 1', 'hostel'): 670000,
    ('Senior 2', 'day'): 360000, ('Senior 2', 'hostel'): 670000,
    ('Senior 3', 'day'): 360000, ('Senior 3', 'hostel'): 670000,
    ('Senior 4', 'day'): 360000, ('Senior 4', 'hostel'): 670000,
    ('Senior 5', 'day'): 380000, ('Senior 5', 'hostel'): 680000,
    ('Senior 6', 'day'): 380000, ('Senior 6', 'hostel'): 680000,
}

METHODS = ['MTN_UG', 'MTN_UG', 'MTN_UG', 'Airtel_UG', 'Airtel_UG', 'Bank Transfer', 'Cash']
TERMS = [('Term 1', '2026'), ('Term 2', '2026')]

print("Clearing old payments...")
cursor.execute("DELETE FROM payments")
conn.commit()

cursor.execute("SELECT payment_code, current_class, category FROM students WHERE status = 'active'")
students = cursor.fetchall()

payment_count = cleared = partial = unpaid = overpaid = 0

def add_payment(code, amount, days_ago_min=1, days_ago_max=160):
    term_info = random.choice(TERMS)
    method = random.choice(METHODS)
    days_ago = random.randint(days_ago_min, days_ago_max)
    pay_date = datetime.now() - timedelta(days=days_ago)
    trans_id = str(random.randint(100000000, 999999999))
    cursor.execute("""
        INSERT INTO payments (payment_code, amount_paid, payment_date, payment_method, transaction_id, term, academic_year)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (code, amount, pay_date, method, trans_id, term_info[0], term_info[1]))
    return 1

for payment_code, class_name, category in students:
    total_fee = FEE_MAP.get((class_name, category), 800000)
    scenario = random.random()
    
    if scenario < 0.15:
        # 15% Not Paid
        unpaid += 1
        continue
        
    elif scenario < 0.25:
        # 10% Overpaid
        overpaid += 1
        # Pay in 1-2 installments
        extra = random.randint(50000, 200000)
        total_to_pay = total_fee + extra
        if random.random() < 0.5:
            payment_count += add_payment(payment_code, total_to_pay)
        else:
            half1 = total_to_pay // 2
            payment_count += add_payment(payment_code, half1)
            payment_count += add_payment(payment_code, total_to_pay - half1)
            
    elif scenario < 0.65:
        # 40% Fully Cleared
        cleared += 1
        if random.random() < 0.4:
            payment_count += add_payment(payment_code, total_fee)
        elif random.random() < 0.7:
            half = total_fee // 2
            payment_count += add_payment(payment_code, half)
            payment_count += add_payment(payment_code, total_fee - half)
        else:
            third = total_fee // 3
            payment_count += add_payment(payment_code, third)
            payment_count += add_payment(payment_code, third)
            payment_count += add_payment(payment_code, total_fee - (third * 2))
            
    else:
        # 35% Partially Paid
        partial += 1
        partial_amount = random.randint(total_fee // 4, total_fee * 3 // 4)
        payment_count += add_payment(payment_code, partial_amount)

conn.commit()

print(f"\n=== PAYMENT SUMMARY ===")
print(f"Total payments created: {payment_count}")
print(f"✅ Fully Cleared:    {cleared} ({round(cleared/len(students)*100,1)}%)")
print(f"⚠ Partially Paid:   {partial} ({round(partial/len(students)*100,1)}%)")
print(f"❌ Not Paid:         {unpaid} ({round(unpaid/len(students)*100,1)}%)")
print(f"💠 Overpaid:         {overpaid} ({round(overpaid/len(students)*100,1)}%)")

cursor.close()
conn.close()
print("\n✅ Done!")