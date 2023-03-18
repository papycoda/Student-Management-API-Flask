from database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Student {self.id}>"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Course {self.id}>"

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)

    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

    def __repr__(self):
        return f"<Enrollment {self.id}>"
