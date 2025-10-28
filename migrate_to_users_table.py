import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Create 'users' table if it doesn't exist
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'teacher'))
);
''')
print("✅ Users table ready.")

# --- Migrate students ---
try:
    students = cur.execute("SELECT * FROM students").fetchall()
    count = 0
    for s in students:
        # s = (id, full_name, username, password)
        full_name = s[1].split(" ", 1)
        first = full_name[0]
        last = full_name[1] if len(full_name) > 1 else ""
        cur.execute(
            "INSERT OR IGNORE INTO users (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, 'student')",
            (first, last, s[2], s[3])
        )
        count += 1
    print(f"✅ Migrated {count} students.")
except sqlite3.OperationalError as e:
    print("⚠️ Could not migrate students:", e)

# --- Migrate teachers ---
try:
    teachers = cur.execute("SELECT * FROM teachers").fetchall()
    count = 0
    for t in teachers:
        # t = (id, full_name, username, password)
        full_name = t[1].split(" ", 1)
        first = full_name[0]
        last = full_name[1] if len(full_name) > 1 else ""
        cur.execute(
            "INSERT OR IGNORE INTO users (first_name, last_name, username, password, role) VALUES (?, ?, ?, ?, 'teacher')",
            (first, last, t[2], t[3])
        )
        count += 1
    print(f"✅ Migrated {count} teachers.")
except sqlite3.OperationalError as e:
    print("⚠️ Could not migrate teachers:", e)

conn.commit()
conn.close()
print("✅ Migration complete.")
