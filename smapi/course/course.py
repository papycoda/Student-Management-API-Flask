from flask_restx import Resource, Namespace, fields
from flask import request
from ..models.course import Course
from ..models.student import Student
from ..models.grades import Grade
from ..models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

course_namespace = Namespace(
    'course', description='CRUD for courses with paths')

course_get_model = course_namespace.model('CoursePlace', {
    'id': fields.Integer(),
    'name': fields.String(required=True, description='Course name', enum=['FrontEnd', 'BackEnd', 'Cloud']),
    'instructor': fields.String(required=True, description='Course instructor')
})


@course_namespace.route('/getall_course')
class GetAllCourses(Resource):
    @jwt_required()
    def get(self):
        '''
         Get all courses in database with Authorization
        '''
        course = {k: f"{v} Engineering" for k, v in {'FrontEnd': 'FrontEnd', 'BackEnd': 'BackEnd', 'Cloud': 'Cloud'}.items()}
        return course, HTTPStatus.OK

# route for getting course by a specific student using their name


@course_namespace.route('/getme/get_course')
class GetCourseBySpecificUser(Resource):
    @course_namespace.marshal_with(course_get_model)
    @jwt_required()
    def get(self):
        '''
            Get courses for a user based on track using Authorization
        '''
        courses = Course.query.filter_by(student=get_jwt_identity().id).all()
        return courses, HTTPStatus.OK


# route for setting up a student course using authorization
@course_namespace.route('/create_course')
class CreateCourse(Resource):
    @course_namespace.expect(course_get_model)
    @course_namespace.marshal_with(course_get_model)
    @jwt_required()
    def post(self):
        '''
            Create Course
        '''

        courses = Course.query.filter_by(student=get_jwt_identity().id).first()

        if courses:
            return 'You are not allowed to create a course again', HTTPStatus.UNAUTHORIZED

        data = course_namespace.payload

        Create_course = Course(
            name=data['name'],
            instructor=data['instructor'],
            student=get_jwt_identity().id
        )

        Create_course.save()
        return Create_course, HTTPStatus.CREATED
