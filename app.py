#draft
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
api = Api(app, security='Bearer Auth')

db = SQLAlchemy(app)

# Define the database models
class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    courses = db.relationship('CourseModel', secondary='registration', backref='students')

class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    students = db.relationship('StudentModel', secondary='registration', backref='courses')
    grades = db.relationship('GradeModel', backref='course')

class RegistrationModel(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student_model.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course_model.id'), primary_key=True)

class GradeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_model.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course_model.id'))

# Define the API models
student_model = api.model('Student', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'student_id': fields.String(required=True),
    'email': fields.String(required=True),
    'courses': fields.List(fields.Integer())
})

course_model = api.model('Course', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'teacher': fields.String(required=True),
    'students': fields.List(fields.Integer()),
    'grades': fields.List(fields.Float())
})

grade_model = api.model('Grade', {
    'id': fields.Integer(),
    'grade': fields.Float(required=True),
    'student_id': fields.Integer(),
    'course_id': fields.Integer()
})

# Define the API endpoints
@api.route('/students')
class StudentList(Resource):
    @api.doc(security='Bearer Auth')
    @api.marshal_list_with(student_model)
    def get(self):
        '''Retrieve a list of all students'''
        pass

    @api.doc(security='Bearer Auth')
    @api.expect(student_model)
    @api.marshal_with(student_model, code=201)
    def post(self):
        '''Create a new student'''
        pass

@api.route('/students/<int:id>')
class Student(Resource):
    @api.doc(security='Bearer Auth')
    @api.marshal_with(student_model)
    def get(self, id):
        '''Retrieve a student by ID'''
        pass

    @api.doc(security='Bearer Auth')
    @api.expect(student_model)
    @api.marshal_with(student_model)
    def put(self, id):
        '''Update a student by ID'''
        pass

    @api.doc(security='Bearer Auth')
    @api
