from flask_restx import Resource, Namespace, fields
from ..models.student import Student
from ..models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

student_namespace = Namespace(
    'Students', description="Authentication for student management api"
)

student_model = student_namespace.model('Students', {
    'id': fields.Integer(readOnly=True, description='Student Identifier',autoincrement=True),
    'name': fields.String(required=True, description='Student name'),
    'email': fields.String(required=True, description='Student email address'),
    'password': fields.String(required=True, description='Student password')
})



#register as student
@student_namespace.route('/signup')
class StudentSignUp(Resource):
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    def post(self):
        '''
            Student Signup
        '''
        data = student_namespace.payload
        name = data['name']
        email = data['email']
        password = data['password']

        new_student = Student(name=name, email=email, password=password)
        new_student.save()

        return new_student, HTTPStatus.CREATED

@student_namespace.route('/')
class GetAllStudents(Resource):
    @jwt_required()
    def get(self):
        '''
            Get All Students
        '''
        current_user_email = get_jwt_identity()
        current_user = Student.query.filter_by(email=current_user_email).first()

        if current_user:
            author_admin = Admin.query.filter_by(email=current_user_email).first()

            if author_admin:
                students = Student.query.all()
                return student_model.dump(students), HTTPStatus.OK
            else:
                return {"message": "You are not authorized to view all students"}, HTTPStatus.UNAUTHORIZED
        else:
            return {"message": "Invalid User"}, HTTPStatus.UNAUTHORIZED

@student_namespace.route('/student/<int:id>')
class StudentResource(Resource):
    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self, id):
        '''
            Get a specific student by ID
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()
        if author_admin or author_student:
            student = Student.query.filter_by(id=id).first()
            if student:
                return student, HTTPStatus.OK
            else:
                return {"message": "Student not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "You are not authorized to view this student"}, HTTPStatus.UNAUTHORIZED

    @student_namespace.expect(student_model)
    @jwt_required()
    def put(self, id):
        '''
            Update a specific student by ID
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()
        if author_admin:
            student = Student.query.filter_by(id=id).first()
            if student:
                data = student_namespace.payload
                student.name = data['name']
                student.email = data['email']
                student.password = data['password']
                student.save()
                return student, HTTPStatus.OK
            else:
                return {"message": "Student not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "You are not authorized to update this student"}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def delete(self, id):
        '''
            Delete a specific student by ID
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        if author_admin:
            student = Student.query.filter_by(id=id).first()
            if student:
                student.delete()
                return {"message": "Student deleted successfully"}, HTTPStatus.OK
            else:
                return {"message": "Student not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "You are not authorized to delete this student"}, HTTPStatus.UNAUTHORIZED
