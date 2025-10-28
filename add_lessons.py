import sqlite3

# Connect to your existing database
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Complete lesson list (in order)
lessons = [
    ("Lesson 1 – Bit Patterns",),
    ("Lesson 2 – Number Bases",),
    ("Lesson 3 – Converting Numbers",),
    ("Lesson 4 – Converting Numbers 2",),
    ("Lesson 5 – Binary Arithmetics",),
    ("Lesson 6 – Binary Arithmetics 2",),
    ("Lesson 7 – Units of Storage",),
    ("Lesson 8 – Representing Images",),
    ("Lesson 9 – Representing Sound",),
    ("Lesson 10 – Compression",),
    ("Lesson 11 – Compression 2",),
    ("Lesson 12 – Encryption",)
]

# Insert lessons if they don’t already exist
cur.executemany('''
INSERT OR IGNORE INTO lessons (title)
VALUES (?)
''', lessons)

conn.commit()
conn.close()

print("✅ All 12 lessons added successfully!")
