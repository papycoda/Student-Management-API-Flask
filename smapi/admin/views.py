from flask_restx import Resource, Namespace, abort
from ..models.student import Student
from ..models.admin import Admin
from ..models.course import Course
from flask import jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import db

admin_namespace = Namespace(
    'auth', description="Admin authentication for deleting student on the management api")

@admin_namespace.route('/delete/<int:id>')
class DeleteStudentById(Resource):
    @jwt_required()
    def delete(self, id):
        '''
        Delete Student by id
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        if not author_admin:
            abort(HTTPStatus.UNAUTHORIZED, message="You are not authorized to delete student")
        student = Student.query.filter_by(id=id).first()
        if not student:
            abort(HTTPStatus.NOT_FOUND, message="Student not found")
        student.delete_by_id(id)
        return {"message": "Student deleted successfully"}, HTTPStatus.NO_CONTENT

@admin_namespace.route('/student/<int:student_id>/course')
class DeleteStudentCourse(Resource):
    @jwt_required()
    def delete(self, student_id):
        '''
        Delete Course for a Student By Admin
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        if not author_admin:
            abort(HTTPStatus.UNAUTHORIZED, message="You are not authorized to delete student course")
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            abort(HTTPStatus.NOT_FOUND, message="Student not found")
        course = Course.query.filter_by(student=student_id).first()
        if not course:
            abort(HTTPStatus.NOT_FOUND, message="Course not found")
        db.session.delete(course)
        db.session.commit()
        return {'message': f'Course deleted for student {student_id}'}, HTTPStatus.NO_CONTENT

@admin_namespace.route('/course/<string:course_name>/students')
class GetStudentPerCourse(Resource):
    @jwt_required()
    def get(self, course_name):
        '''
        Get student registered in each course
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        if not author_admin:
            abort(HTTPStatus.UNAUTHORIZED, message="You are not authorized to view students per course")
        course = Course.query.filter_by(name=course_name).first()
        if not course:
            abort(HTTPStatus.NOT_FOUND, message="Course not found")
        students = course.student
        return {'students': students}, HTTPStatus.OK
