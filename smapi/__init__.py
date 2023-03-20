from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import BadRequest, InternalServerError, MethodNotAllowed, NotFound
from datetime import timedelta

from .auth.views import admin_auth_namespace
from .course.course import course_namespace
from .admin.views import admin_namespace
from .students.views import student_namespace
from .utils import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY='d961e034c39e798bbf0f2a6c',
        JWT_SECRET_KEY='c961e054c69e798bbf0f2a5c',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7),
        SQLALCHEMY_DATABASE_URI='sqlite:///api.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    migrate = Migrate(app, db)

    api = Api(
        app,
        title='Student Management API',
        description='student management api with basic crud operations',
        prefix='/api'
    )

    api.add_namespace(admin_auth_namespace, path='/auth/admin')
    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(student_namespace)
    api.add_namespace(admin_namespace, path='/admin')

    @api.errorhandler(BadRequest)
    def handle_bad_request_error(error):
        return {'message': 'Bad Request Error'}, 400

    @api.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        return {'message': 'Database Error'}, 500

    @api.errorhandler(NotFound)
    def handle_not_found_error(error):
        return {'message': 'Not Found'}, 404

    @api.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed_error(error):
        return {'message': 'Method Not Allowed'}, 405

    return app
