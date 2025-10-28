import sqlite3

# Connect to your database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Add a teacher account
cursor.execute('''
INSERT OR IGNORE INTO teachers (name, username, password)
VALUES (?, ?, ?)
''', ("Dinos", "teacher", "1234"))

# Add some student accounts
students = [
    ("Alice Johnson", "student1", "pass1"),
    ("Bob Smith", "student2", "pass2")
]

cursor.executemany('''
INSERT OR IGNORE INTO students (name, username, password)
VALUES (?, ?, ?)
''', students)

# Save and close
connection.commit()
connection.close()

print("✅ Sample teacher and student accounts added successfully!")
