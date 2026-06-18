import pymysql

conn = pymysql.connect(
    host='localhost',
    user='onecard_user',
    password='OneCard@2026',
    database='school_test_db'
)
cursor = conn.cursor()

# Count with photos
cursor.execute("SELECT COUNT(*) FROM students WHERE photo_path IS NOT NULL AND photo_path != ''")
with_photos = cursor.fetchone()[0]

# Total active
cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'active'")
total = cursor.fetchone()[0]

# Show first 10
cursor.execute("""
    SELECT admission_number, full_name, current_class, stream, photo_path 
    FROM students 
    WHERE photo_path IS NOT NULL AND photo_path != '' 
    LIMIT 10
""")

print(f"\n=== STUDENTS WITH PHOTOS ===")
print(f"{with_photos} out of {total} active students have photos ({round(with_photos/total*100, 1)}%)\n")
print(f"{'Admission':<15} {'Name':<25} {'Class':<12} {'Stream':<6} {'Photo Path'}")
print('-' * 80)
for row in cursor.fetchall():
    print(f"{row[0]:<15} {row[1]:<25} {row[2]:<12} {row[3]:<6} {row[4]}")

cursor.close()
conn.close()