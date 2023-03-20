from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.admin import Admin
from ..models.course import Course
from ..models.grades import Grade
from ..models.student import Student
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus

admin_auth_namespace = Namespace(
    'admin_auth', description="Authentication for admin")

admin_model = admin_auth_namespace.model('Admin', {
    'email': fields.String(required=True, description='Admin email address'),
    'password': fields.String(required=True, description='Admin password'),
    'type_acct': fields.String(required=True, description='Admin account type', default='admin')
})

admin_login_model = admin_auth_namespace.model('Login_Admin', {
    'email': fields.String(required=True, description='Admin email address'),
    'password': fields.String(required=True, description='Admin password'),
})

course_model = admin_auth_namespace.model('Course', {
    'name': fields.String(required=True, description='Course name'),
    'instructor': fields.String(required=True, description='Course instructor'),
    'student_id': fields.Integer(required=True, description='ID of student taking the course'),
})

grade_model = admin_auth_namespace.model('Grade', {
    'score': fields.String(required=True, description='Grade for student'),
    'student_id': fields.Integer(required=True, description='ID of student'),
    'course_id': fields.Integer(required=True, description='ID of course'),
})

@admin_auth_namespace.route('/signup')
class AdminSignUp(Resource):
    @admin_auth_namespace.expect(admin_model)
    @admin_auth_namespace.marshal_with(admin_model)
    def post(self):
        '''
            Authenticate Signup for admin
        '''
        data = request.get_json()
        email = data['email']
        type_acct = data['type_acct']
        password = generate_password_hash(data['password'])

        new_admin = Admin(email=email, password=password, type_acct=type_acct)
        new_admin.save()

        return new_admin, HTTPStatus.CREATED


@admin_auth_namespace.route('/login')
class AdminLogin(Resource):
    @admin_auth_namespace.expect(admin_login_model)
    def post(self):
        '''
            Authenticate Login for admin
        '''
        data = admin_auth_namespace.payload
        email = data['email']
        user = Admin.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            response = {
                'create_access_token': access_token,
                'create_refresh_token': refresh_token,
                'type': 'admin'
            }

            return response, HTTPStatus.CREATED


@admin_auth_namespace.route('/courses')
class AdminCourse(Resource):
    @jwt_required()
    def get(self):
        '''
            Get all courses
        '''
        courses = Course.query.all()
        return courses

    @admin_auth_namespace.expect(course_model)
    @jwt_required()
    def post(self):
        '''
            Add a new course
        '''
        data = request.get_json()
        name = data['name']
        instructor = data['instructor']
        student_id = data['student_id']

        course = Course(name=name, instructor=instructor, student=student_id)
        course.save()

        return course, HTTPStatus.CREATED

    @admin_auth_namespace.expect(course_model)
    @jwt_required()
    def put(self):
        '''
            Update an existing course.
        '''
        admin_email = get_jwt_identity()
        admin = Admin.query.filter_by(email=admin_email).first()
        if admin.type_acct != 'admin':
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED
        data = request.get_json()
        course_id = data['id']
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return {"message": "Course not found"}, HTTPStatus.NOT_FOUND

        course.name = data['name']
        course.instructor = data['instructor']
        course.save()

        return course, HTTPStatus.OK
    
    @admin_auth_namespace.expect(course_model)
    @jwt_required()
    def delete(self, course_id):
        '''
            Delete an existing course.
        '''
        admin_email = get_jwt_identity()
        admin = Admin.query.filter_by(email=admin_email).first()
        if admin.type_acct != 'admin':
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return {"message": "Course not found"}, HTTPStatus.NOT_FOUND

        course.delete()

        return {"message": "Course deleted"}, HTTPStatus.OK
    
@admin_auth_namespace.route('/course/add_grade/int:course_id/int:student_id')
class AdminAddGrade(Resource):
    @admin_auth_namespace.expect(grade_model)
    @jwt_required()
    def post(self, course_id, student_id):
        '''
        Add grade for a student in a course.
        '''
        admin_email = get_jwt_identity()
        admin = Admin.query.filter_by(email=admin_email).first()
        if admin.type_acct != 'admin':
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            return {"message": "Course not found"}, HTTPStatus.NOT_FOUND

        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {"message": "Student not found"}, HTTPStatus.NOT_FOUND

        data = request.get_json()
        grade_score = data['score']
        new_grade = Grade(score=grade_score, student=student_id)
        new_grade.save()

        return new_grade, HTTPStatus.CREATED
        

@admin_auth_namespace.route('/course/edit_grade/int:grade_id')
class AdminEditGrade(Resource):
    @admin_auth_namespace.expect(grade_model)
    @jwt_required()
    def put(self, grade_id):
        '''
        Update an existing grade.
        '''
        admin_email = get_jwt_identity()
        admin = Admin.query.filter_by(email=admin_email).first()
        if admin.type_acct != 'admin':
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED
        grade = Grade.query.filter_by(id=grade_id).first()   
        if not grade:
            return {"message": "Grade not found"}, HTTPStatus.NOT_FOUND
        data = request.get_json()
        grade_score = data['score']
        grade.score = grade_score
        grade.save()

        return grade, HTTPStatus.OK
    
@admin_auth_namespace.route('/course/delete_grade/int:grade_id')
class AdminDeleteGrade(Resource):
    @jwt_required()
    def delete(self, grade_id):
        '''
        Delete an existing grade.
        '''
        admin_email = get_jwt_identity()
        admin = Admin.query.filter_by(email=admin_email).first()
        if admin.type_acct != 'admin':
            return {"message": "Not authorized"}, HTTPStatus.UNAUTHORIZED
        grade = Grade.query.filter_by(id=grade_id).first()
        if not grade:
            return {"message": "Grade not found"}, HTTPStatus.NOT_FOUND

        grade.delete()

        return {"message": "Grade deleted"}, HTTPStatus.OK