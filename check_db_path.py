import sqlite3, os

conn = sqlite3.connect('database.db')
print("✅ Using database file at:")
print(os.path.abspath('database.db'))

cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("\n📋 Tables found in this database:")
for row in cur.fetchall():
    print("-", row[0])

conn.close()
