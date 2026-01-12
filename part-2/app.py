from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3  # Built-in Python library for SQLite database

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

DATABASE = 'students.db'  # Database file name (will be created automatically)


# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================

def get_db_connection():
    """Create a connection to the database"""
    conn = sqlite3.connect(DATABASE)  # Connect to database file
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name (like dict)
    return conn


def init_db():
    """Create the table if it doesn't exist"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')  # SQL command to create table with 4 columns
    conn.commit()  # Save changes to database
    conn.close()  # Close connection


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Home page - Display all students from database"""
    try:
        conn = get_db_connection()  # Step 1: Connect to database
        students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()  # Step 2: Get all rows (newest first)
        conn.close()  # Step 3: Close connection
        return render_template('index.html', students=students)
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'error')
        return render_template('index.html', students=[])


@app.route('/add_sample')
def add_sample_student():
    """Add multiple sample students to database (for testing)"""
    sample_students = [
        ('John Doe', 'john@example.com', 'Python'),
        ('Jane Smith', 'jane@example.com', 'JavaScript'),
        ('Bob Johnson', 'bob@example.com', 'Java'),
        ('Alice Williams', 'alice@example.com', 'Python'),
        ('Charlie Brown', 'charlie@example.com', 'C++'),
        ('Diana Prince', 'diana@example.com', 'Web Development')
    ]
    
    try:
        conn = get_db_connection()
        for name, email, course in sample_students:
            conn.execute(
                'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
                (name, email, course)  # ? are placeholders (safe from SQL injection)
            )
        conn.commit()  # Don't forget to commit!
        conn.close()
        flash(f'Successfully added {len(sample_students)} sample students!', 'success')
    except Exception as e:
        flash(f'Error adding students: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student via form"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        
        # Validation
        if not name or not email or not course:
            flash('All fields are required!', 'error')
            return render_template('add_student.html')
        
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
                (name, email, course)
            )
            conn.commit()
            conn.close()
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'error')
    
    return render_template('add_student.html')


if __name__ == '__main__':
    init_db()  # Create table when app starts
    app.run(debug=True)

