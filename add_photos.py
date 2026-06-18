"""
Download AI-generated student photos and update the school database.
Run: python add_photos.py
"""
import pymysql
import requests
import os
import time

# ============================================
# DATABASE CONNECTION
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'onecard_user',
    'password': 'OneCard@2026',
    'database': 'school_test_db',
    'charset': 'utf8mb4'
}

# ============================================
# PHOTO STORAGE PATH
# ============================================
PHOTO_DIR = r'C:\Users\jaing\projects\onecard_system\media\student_photos'
os.makedirs(PHOTO_DIR, exist_ok=True)

# ============================================
# HOW MANY STUDENTS?
# ============================================
NUM_STUDENTS = 250  # Change this number

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Get students without photos
    cursor.execute("""
        SELECT admission_number FROM students 
        WHERE status = 'active' 
        AND (photo_path IS NULL OR photo_path = '')
        LIMIT %s
    """, [NUM_STUDENTS])
    
    students = [row[0] for row in cursor.fetchall()]
    print(f"Found {len(students)} students without photos.\n")
    print("Downloading AI-generated faces...\n")
    
    count = 0
    for admission in students:
        photo_filename = f"{admission}.jpg"
        photo_full_path = os.path.join(PHOTO_DIR, photo_filename)
        
        # Skip if already downloaded
        if os.path.exists(photo_full_path):
            count += 1
            continue
        
        try:
            # Download AI face
            r = requests.get('https://thispersondoesnotexist.com/', timeout=15)
            if r.status_code == 200:
                # Save file
                with open(photo_full_path, 'wb') as f:
                    f.write(r.content)
                
                # Update database with relative path
                photo_db_path = f"student_photos/{photo_filename}"
                cursor.execute(
                    "UPDATE students SET photo_path = %s WHERE admission_number = %s",
                    [photo_db_path, admission]
                )
                conn.commit()
                
                count += 1
                if count % 25 == 0:
                    print(f"  ✅ {count}/{len(students)} done...")
                
                time.sleep(0.3)  # Be nice to the server
                
        except Exception as e:
            print(f"  ❌ {admission}: {e}")
            time.sleep(1)
    
    cursor.close()
    conn.close()
    
    print(f"\n🎉 COMPLETE! {count} photos downloaded.")
    print(f"   Photos saved to: {PHOTO_DIR}")
    print(f"   Database updated for all students.")

if __name__ == '__main__':
    main()