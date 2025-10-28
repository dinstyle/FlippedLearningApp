import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

columns = ["mark_video", "mark_workbook", "mark_interactive", "mark_exam"]

for col in columns:
    try:
        cur.execute(f"ALTER TABLE progress ADD COLUMN {col} INTEGER;")
        print(f"✅ Added column: {col}")
    except sqlite3.OperationalError:
        print(f"ℹ️ Column {col} already exists, skipping.")

conn.commit()
conn.close()
print("✅ Mark columns added (or already existed).")
