from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request, get_jwt
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Student Management API',
    description='A simple API for managing students, courses, and enrollments'
)

REGISTERED_USERS = {}


# Define your roles and associated permissions
ROLES_PERMISSIONS = {
    'student': ['view_own_profile'],
    'admin': ['create_students', 'delete_students', 'view_all_profiles']
}

# Define the roles_required decorator to check for the required roles
def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # Check that the JWT is valid
            verify_jwt_in_request()

            # Get the user's roles from the JWT claims
            claims = get_jwt()
            user_roles = claims.get('roles', [])

            # Check that the user has all the required roles
            for role in roles:
                if role not in user_roles:
                    return {'message': 'You are not authorized to perform this action'}, 403

                # Check that the user has all the required permissions for this role
                if not set(ROLES_PERMISSIONS[role]).issubset(set(claims.keys())):
                    return {'message': 'You are not authorized to perform this action'}, 403

            # If the user has all the required roles and permissions, call the view function
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Student data access object
class StudentDAO(object):
    def __init__(self):
        self.counter = 0
        self.students = []

    def get(self, id):
        for student in self.students:
            if student['id'] == id:
                return student
        api.abort(404, "Student {} doesn't exist".format(id))

    def create(self, data):
        student = data
        student['id'] = self.counter = self.counter + 1
        self.students.append(student)
        return student

    def update(self, id, data):
        student = self.get(id)
        student.update(data)
        return student

    def delete(self, id):
        student = self.get(id)
        self.students.remove(student)

# Course data access object
class CourseDAO(object):
    def __init__(self):
        self.counter = 0
        self.courses = []

    def get(self, id):
        for course in self.courses:
            if course['id'] == id:
                return course
        api.abort(404, "Course {} doesn't exist".format(id))

    def create(self, data):
        course = data
        course['id'] = self.counter = self.counter + 1
        self.courses.append(course)
        return course

    def update(self, id, data):
        course = self.get(id)
        course.update(data)
        return course

    def delete(self, id):
        course = self.get(id)
        self.courses.remove(course)

# Enrollment data access object
class EnrollmentDAO(object):
    def __init__(self):
        self.counter = 0
        self.enrollments = []

    def get(self, id):
        for enrollment in self.enrollments:
            if enrollment['id'] == id:
                return enrollment
        api.abort(404, "Enrollment {} doesn't exist".format(id))

    def create(self, data):
        enrollment = data
        enrollment['id'] = self.counter = self.counter + 1
        self.enrollments.append(enrollment)
        return enrollment

    def update(self, id, data):
        enrollment = self.get(id)
        enrollment.update(data)
        return enrollment

    def delete(self, id):
        enrollment = self.get(id)
        self.enrollments.remove(enrollment)

# Models
student = api.model('Student', {
    'id': fields.Integer(readonly=True, description='The student unique identifier'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email'),
    'phone': fields.String(required=True, description='The student phone number'),
    'gpa': fields.Float(required=True, description='The student GPA'),
})

course = api.model('Course', {
    'id': fields.Integer(readonly=True, description='The course unique identifier'),
    'name': fields.String(required=True, description='The course name'),
    'description': fields.String(required=True, description='The course description'),
    'credits': fields.Integer(required=True, description='The number of credits for the course'),
    'instructor': fields.String(required=True, description='The instructor for the course'),
})

enrollment = api.model('Enrollment', {
    'id': fields.Integer(readonly=True, description='The enrollment unique identifier'),
    'student_id': fields.Integer(required=True, description='The ID of the student'),
    'course_id': fields.Integer(required=True, description='The ID of the course'),
})

user_details = api.model('UserDetails', {
    'username': fields.String(required=True, description='The user\'s username'),
    'password': fields.String(required=True, description='The user\'s password'),
    'role': fields.String(description='The user\'s role (default is student)')
})


# DAOs
STUDENTS = StudentDAO()
COURSES = CourseDAO()
ENROLLMENTS = EnrollmentDAO()


# Data
COURSES = {
    'courses': [
        {'id': 1, 'name': 'Course 1', 'description': 'Course 1 description', 'credits': 3, 'instructor': 'John Doe'},
        {'id': 2, 'name': 'Course 2', 'description': 'Course 2 description', 'credits': 4, 'instructor': 'Jane Smith'}
    ]
}

STUDENTS = {
    'students': [
        {'id': 1, 'name': 'Student 1', 'email': 'student1@example.com', 'phone': '123-456-7890', 'gpa': 3.5},
        {'id': 2, 'name': 'Student 2', 'email': 'student2@example.com', 'phone': '123-456-7891', 'gpa': 4.0},
        {'id': 3, 'name': 'Student 3', 'email': 'student3@example.com', 'phone': '123-456-7892', 'gpa': 3.0},
    ]
}

#auth endpoints
@api.route('/register')
class UserRegistration(Resource):

    @api.doc('register')
    @api.expect(user_details)
    @api.marshal_with(user_details, code=201)
    def post(self):
        '''Register a new user'''
        data = api.payload
        username = data['username']
        password = data['password']
        role = data.get('role', 'student')  # default role is student if not specified

        # Check if the username already exists in the registered users
        if username in REGISTERED_USERS:
            return {'message': 'Username already exists'}, 400

        # Add the new user to the registered users
        REGISTERED_USERS[username] = {'password': password, 'role': role}

        # Return the newly registered user with a success message
        return {'username': username, 'role': role, 'message': 'User successfully registered'}, 201
    
@api.route('/login')
class UserLogin(Resource):
    
        @api.doc('login')
        @api.expect(user_details)
        def post(self):
            '''Login a user'''
            data = api.payload
            username = data['username']
            password = data['password']
    
            # Check if the username exists in the registered users
            if username not in REGISTERED_USERS:
                return {'message': 'Username does not exist'}, 400
    
            # Check if the password is correct
            if password != REGISTERED_USERS[username]['password']:
                return {'message': 'Incorrect password'}, 400
    
            # Create a new token
            access_token = create_access_token(identity=username)
    
            # Return the token with a success message
            return {'message': 'User successfully logged in', 'access_token': access_token}, 200



# Student endpoints

@api.route('/students')
class StudentList(Resource):

    @api.doc('list_students')
    @api.marshal_list_with(student)
    @jwt_required

    def get(self):
        '''List all students'''
        return STUDENTS['students']


    @api.doc('create_student')
    @api.expect(student)
    @api.marshal_with(student, code=201)
    @jwt_required

    def post(self):
        '''Create a new student'''
        return STUDENTS.create(api.payload), 201
    
@api.route('/students/<int:id>')
@api.response(404, 'Student not found')
@api.param('id', 'The student identifier')
class Student(Resource):
    @api.doc('get_student')
    @api.marshal_with(student)
    @jwt_required
    @roles_required('student', 'admin')
    def get(self, id):
        '''Fetch a student given its identifier if the user is a student or an admin else return 403'''
        
        if get_jwt_identity() != 'admin' and get_jwt_identity() != id:
            return {'message': 'You are not authorized to access this resource'}, 403
        else:
            return STUDENTS.get(id)
    
    @api.doc('delete_student')
    @api.response(204, 'Student deleted')
    @jwt_required
    @roles_required('admin')
    def delete(self, id):
        '''Delete a student given its identifier'''
        STUDENTS.delete(id)
        return '', 204
    
    @api.expect(student)
    @api.marshal_with(student)
    @jwt_required
    @roles_required('admin')
    def put(self, id):
        '''Update a student given its identifier'''
        return STUDENTS.update(id, api.payload)
    
# Course endpoints
@api.route('/courses')
class CourseList(Resource):
    @api.doc('list_courses')
    @api.marshal_list_with(course)
    def get(self):
        '''List all courses'''
        return COURSES['courses']
    
    @api.doc('create_course')
    @api.expect(course)
    @api.marshal_with(course, code=201)
    @jwt_required
    @roles_required('admin')
    def post(self):
        '''Create a new course'''
        return COURSES.create_course(api.payload), 201


@api.route('/courses/<int:id>')
@api.response(404, 'Course not found')
@api.param('id', 'The course identifier')
class Course(Resource):
    @api.doc('get_course')
    @api.marshal_with(course)
    
    def get(self, id):
        '''Fetch a course given its identifier'''
        return COURSES.get_course(id)
    
    @api.doc('update_course')
    @api.expect(course)
    @api.marshal_with(course)
    @jwt_required
    @roles_required('admin')
    def put(self, id):
        '''Update a course given its identifier'''
        return COURSES.update_course(id, api.payload)
    
    @api.doc('delete_course')
    @api.response(204, 'Course deleted')
    @jwt_required
    @roles_required('admin')
    def delete(self, id):
        '''Delete a course given its identifier'''
        COURSES.delete_course(id)
        return '', 204


@api.route('/students/<int:student_id>/courses')
@api.response(404, 'Student not found')
@api.param('student_id', 'The student identifier')
class StudentCourses(Resource):
    @api.doc('list_student_courses')
    @api.marshal_list_with(course)
    def get(self, student_id):
        '''List all courses of a student'''
        student = STUDENTS.get(student_id)
        return [COURSES.get(course_id) for course_id in student['courses']]
    
    @api.doc('enroll_student_in_course')
    @api.expect(student)
    @api.marshal_with(enrollment, code=201)
    @jwt_required
    @roles_required( 'admin')
    def post(self, student_id):
        '''Enroll a student in a course'''
        data = api.payload
        data['student_id'] = student_id
        return ENROLLMENTS.create(data), 201
    
@api.route('/students/<int:student_id>/courses/<int:course_id>')
@api.response(404, 'Enrollment not found')
@api.param('student_id', 'The student identifier')
@api.param('course_id', 'The course identifier')
class StudentCourse(Resource):
    @api.doc('unenroll_student_from_course')
    @api.response(204, 'Enrollment deleted')
    @jwt_required
    @roles_required('admin')
    def delete(self, student_id, course_id):
        '''Unenroll a student from a course'''
        enrollment = ENROLLMENTS.get(student_id, course_id)
        ENROLLMENTS.delete(enrollment)
        return '', 204
    
# Course endpoints  
@api.route('/courses/<int:course_id>/students')
@api.response(404, 'Course not found')
@api.param('course_id', 'The course identifier')
class CourseStudents(Resource):
    @api.doc('list_course_students')
    @api.marshal_list_with(student)
    @jwt_required
    @roles_required('admin')

    def get(self, course_id):
        '''List all students of a course along with their grades'''
        course = COURSES.get_course(course_id)
        #get the students and their grades for the course if they exist
        return [STUDENTS.get(student_id) for student_id in course['students']]
    
    @api.doc('add_student_grade')
    @api.expect(course)
    @api.marshal_with(enrollment, code=201)
    @jwt_required
    @roles_required('admin')
    def post(self, course_id):
        '''Add a student grade to a course'''
        data = api.payload
        data['course_id'] = course_id
        return ENROLLMENTS.create(data), 201
    
@api.route('/courses/<int:course_id>/students/<int:student_id>')
@api.response(404, 'Enrollment not found')
@api.param('course_id', 'The course identifier')
@api.param('student_id', 'The student identifier')

class CourseStudent(Resource):
    @api.doc('delete_student_grade')
    @api.response(204, 'Enrollment deleted')
    @jwt_required
    @roles_required('admin')
    def delete(self, course_id, student_id):
        '''Delete a student grade from a course'''
        enrollment = ENROLLMENTS.get(student_id, course_id)
        ENROLLMENTS.delete(enrollment)
        return '', 204
    
#calculate gpa
@api.route('/students/<int:id>/gpa')
@api.param('id', 'The student identifier')
class CalculateGPA(Resource):
    @api.doc('calculate_gpa')
    def get(self, id):
        '''Calculate the GPA of the student with the given id'''
        student = next((s for s in STUDENTS['students'] if s['id'] == id), None)
        if student:
            return {'gpa': student['gpa']}
        else:
            api.abort(404, f"Student with id {id} not found")

    
if __name__ == '__main__':
    app.run(debug=True)

