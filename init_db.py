import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
''')

# Teachers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
''')

# Lessons table
cursor.execute('''
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);
''')

# Progress table
cursor.execute('''
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    lesson_id INTEGER,
    watched_video INTEGER DEFAULT 0,
    workbook_done INTEGER DEFAULT 0,
    interactive_done INTEGER DEFAULT 0,
    exam_answer TEXT,
    mark_video INTEGER DEFAULT 0,
    mark_workbook INTEGER DEFAULT 0,
    mark_interactive INTEGER DEFAULT 0,
    mark_exam INTEGER DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);
''')

connection.commit()
connection.close()

print("✅ Database and all tables created successfully!")
