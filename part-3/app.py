from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)

    # One teacher -> many courses
    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return f'<Teacher {self.name}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Foreign Key to Teacher
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    # One Course -> Many Students
    students = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Foreign key to Course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'



@app.route('/')
def index():
    # Order students by name
    students = Student.query.order_by(Student.name).all()
    return render_template('index.html', students=students)


@app.route('/courses')
def courses():
    # Show latest courses first
    all_courses = Course.query.order_by(Course.id.desc()).all()
    return render_template('courses.html', courses=all_courses)


@app.route('/teachers')
def teachers():
    all_teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template('teachers.html', teachers=all_teachers)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']

        new_student = Student(name=name, email=email, course_id=course_id)
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)


@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        teacher_id = request.form.get('teacher_id')

        new_course = Course(
            name=name,
            description=description,
            teacher_id=teacher_id if teacher_id else None
        )

        db.session.add(new_course)
        db.session.commit()

        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))

    # THIS WAS MISSING 👇
    teachers = Teacher.query.all()
    return render_template('add_course.html', teachers=teachers)



@app.route('/add-teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        teacher = Teacher(name=name, email=email)
        db.session.add(teacher)
        db.session.commit()

        flash('Teacher added!', 'success')
        return redirect(url_for('teachers'))

    return render_template('add_teacher.html')



def init_db():
    with app.app_context():
        db.create_all()

        # Add sample teachers
        if Teacher.query.count() == 0:
            t1 = Teacher(name="Amit Sharma", email="amit@gmail.com")
            t2 = Teacher(name="Neha Verma", email="neha@gmail.com")

            db.session.add_all([t1, t2])
            db.session.commit()

        # Add sample courses
        if Course.query.count() == 0:
            c1 = Course(name="Python Basics", description="Learn Python", teacher_id=1)
            c2 = Course(name="Web Development", description="Flask + HTML", teacher_id=2)
            c3 = Course(name="Data Science", description="Pandas & ML", teacher_id=1)

            db.session.add_all([c1, c2, c3])
            db.session.commit()

        # Add sample students
        if Student.query.count() == 0:
            s1 = Student(name="Rahul", email="rahul@gmail.com", course_id=1)
            s2 = Student(name="Pooja", email="pooja@gmail.com", course_id=2)
            s3 = Student(name="Aman", email="aman@gmail.com", course_id=1)

            db.session.add_all([s1, s2, s3])
            db.session.commit()

        print("Database initialized with sample data!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
