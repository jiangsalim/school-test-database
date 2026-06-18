import pymysql
import os

PHOTO_DIR = r'C:\Users\jaing\projects\onecard_system\media\student_photos'

conn = pymysql.connect(
    host='localhost',
    user='onecard_user',
    password='OneCard@2026',
    database='school_test_db'
)
cursor = conn.cursor()

# Get all students
cursor.execute("SELECT admission_number FROM students WHERE status = 'active'")
students = [row[0] for row in cursor.fetchall()]

updated = 0
for admission in students:
    photo_filename = f"{admission}.jpg"
    photo_full_path = os.path.join(PHOTO_DIR, photo_filename)
    
    if os.path.exists(photo_full_path):
        photo_db_path = f"student_photos/{photo_filename}"
        cursor.execute(
            "UPDATE students SET photo_path = %s WHERE admission_number = %s",
            [photo_db_path, admission]
        )
        updated += 1

conn.commit()
cursor.close()
conn.close()

print(f"✅ Updated {updated} students with photo paths!")