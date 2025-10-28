import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# 13 precise workbook columns
columns = [
    # Task 1 – 1-bit image
    "t1q1", "t1q2", "t1q3", "t1q4", "t1q5", "t1q6",
    # Task 2 – 2-bit image
    "t2q1", "t2q2", "t2q3",
    # Task 3 – 3-bit image
    "t3q1", "t3q2", "t3q3",
    # Task 4 – binary conversion
    "t4q1"
]

for col in columns:
    try:
        cur.execute(f"ALTER TABLE progress ADD COLUMN {col} TEXT;")
        print(f"✅ Added column: {col}")
    except sqlite3.OperationalError:
        print(f"ℹ️ Column {col} already exists, skipping.")

conn.commit()
conn.close()
print("✅ Workbook columns added (or already existed).")
