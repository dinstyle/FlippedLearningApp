from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn
app.secret_key = "supersecretkey"  # needed for sessions
def get_current_user_id():
    return session.get("user_id")

# Step 1: Simple in-memory user storage (we'll use a database later)
users = {
    "teacher": {"password": "1234", "role": "teacher"},
    "student": {"password": "abcd", "role": "student"}
}

@app.route('/')
def home():
    return render_template('home.html')

# Step 2: Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['username'] = user['username']
            session['role'] = user['role']
            session['user_id'] = user['id']

            if user['role'] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))

        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')



# Step 3: Teacher dashboard
@app.route('/teacher')
def teacher_dashboard():
    if 'username' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login'))

    conn = get_db_connection()
    lessons = conn.execute('SELECT * FROM lessons').fetchall()
    conn.close()

    return render_template(
        'teacher_dashboard.html',
        user=session['username'],
        lessons=lessons
    )


# Step 4: Student dashboard
@app.route('/student')
def student_dashboard():
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    conn = get_db_connection()
    lessons = conn.execute('SELECT * FROM lessons').fetchall()
    conn.close()

    return render_template(
        'dashboard.html',
        user=session['username'],
        role='Student',
        lessons=lessons
    )

@app.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def lesson_page(lesson_id):
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    conn = get_db_connection()

    # Get lesson data
    lesson = conn.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
    student_id = get_current_user_id()

    # Try to get existing record
    progress = conn.execute('SELECT * FROM progress WHERE student_id = ? AND lesson_id = ?', (student_id, lesson_id)).fetchone()

    # Workbook fields (13 total)
    workbook_fields = [
        "t1q1", "t1q2", "t1q3", "t1q4", "t1q5", "t1q6",
        "t2q1", "t2q2", "t2q3",
        "t3q1", "t3q2", "t3q3",
        "t4q1"
    ]

    # Fill defaults
    wb_answers = {f: (progress[f] if progress and progress[f] else '') for f in workbook_fields}

    watched = progress['watched_video'] if progress else 0
    interactive_done = progress['interactive_done'] if progress else 0
    exam_answer = progress['exam_answer'] if progress else ''

    # Handle POST (form submission)
    if request.method == 'POST':
        watched = 1 if 'watched' in request.form else 0
        interactive_done = 1 if 'interactive_done' in request.form else 0
        exam_answer = request.form.get('exam_answer', '')

        # get workbook inputs
        for f in workbook_fields:
            wb_answers[f] = request.form.get(f, '')

        if progress:
            # Update existing
            set_clause = ', '.join([f"{col} = ?" for col in workbook_fields])
            values = list(wb_answers.values()) + [watched, interactive_done, exam_answer, student_id, lesson_id]
            conn.execute(f'''
                UPDATE progress
                SET {set_clause},
                    watched_video = ?,
                    interactive_done = ?,
                    exam_answer = ?
                WHERE student_id = ? AND lesson_id = ?
            ''', values)
        else:
            # Insert new
            cols = ', '.join(workbook_fields)
            placeholders = ', '.join(['?'] * len(workbook_fields))
            values = list(wb_answers.values()) + [watched, interactive_done, exam_answer, student_id, lesson_id]
            conn.execute(f'''
                INSERT INTO progress ({cols}, watched_video, interactive_done, exam_answer, student_id, lesson_id)
                VALUES ({placeholders}, ?, ?, ?, ?, ?)
            ''', values)

        conn.commit()

    # reload updated record
    progress = conn.execute('SELECT * FROM progress WHERE student_id = ? AND lesson_id = ?', (student_id, lesson_id)).fetchone()
    conn.close()

    return render_template(
        'lesson.html',
        lesson_title=lesson['title'],
        video_url="https://craigndave.org/videos/gcse-aqa-slr13-representing-images/",
        watched=bool(watched),
        interactive_done=bool(interactive_done),
        exam_answer=exam_answer,
        wb_answers=wb_answers
    )

@app.route('/teacher/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def teacher_lesson_view(lesson_id):
    conn = get_db_connection()

    # Get lesson info
    lesson = conn.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()

    # Get all students
    students = conn.execute('SELECT * FROM users WHERE role = "student"').fetchall()

    # Get all progress records for this lesson
    progress_records = conn.execute(
        'SELECT * FROM progress WHERE lesson_id = ?',
        (lesson_id,)
    ).fetchall()

    conn.close()

    # Convert progress data into a dictionary {student_id: record}
    progress_data = {p['student_id']: p for p in progress_records}

    return render_template(
        'teacher_lesson.html',
        lesson=lesson,
        students=students,
        progress_data=progress_data
    )
    
@app.route('/teacher/lesson/<int:lesson_id>/student/<int:student_id>', methods=['GET', 'POST'])
def teacher_mark_student(lesson_id, student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM users WHERE id = ?', (student_id,)).fetchone()
    lesson = conn.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()

    # Fetch student's progress
    progress = conn.execute(
        'SELECT * FROM progress WHERE student_id = ? AND lesson_id = ?',
        (student_id, lesson_id)
    ).fetchone()

    if request.method == 'POST':
        mark_video = request.form.get('mark_video', 0)
        mark_workbook = request.form.get('mark_workbook', 0)
        mark_interactive = request.form.get('mark_interactive', 0)
        mark_exam = request.form.get('mark_exam', 0)

        conn.execute('''
            UPDATE progress
            SET mark_video = ?, mark_workbook = ?, mark_interactive = ?, mark_exam = ?
            WHERE student_id = ? AND lesson_id = ?
        ''', (mark_video, mark_workbook, mark_interactive, mark_exam, student_id, lesson_id))
        conn.commit()

        return redirect(url_for('teacher_lesson_view', lesson_id=lesson_id))

    conn.close()
    return render_template(
        'teacher_mark_student.html',
        student=student,
        lesson=lesson,
        progress=progress,
        lesson_id=lesson_id
    )



# Step 5: Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)