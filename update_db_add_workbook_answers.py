import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Add a workbook_answers column if it doesn’t exist yet
try:
    cur.execute('ALTER TABLE progress ADD COLUMN workbook_answers TEXT;')
    print("✅ Added 'workbook_answers' column successfully!")
except sqlite3.OperationalError:
    print("ℹ️ Column already exists, skipping.")

conn.commit()
conn.close()
