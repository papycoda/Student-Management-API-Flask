# Student Management API

The Student Management API is a RESTful API that allows you to manage students, courses, and enrollments. It's built with Flask and Flask-RESTful and can be accessed through the following endpoint:

Papycoda.pythonanywhere.com/api/v1

## Prerequisites

Python version: Python 3.11

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and activate it:

```console
python -m venv venv
source venv/bin/activate
```

Install the dependencies:
```console

pip install -r requirements.txt
```

Run the application:
```console
python runserver.py
```
To start operations with the database and navigate through some API endpoints, the user must be authorized by using the login and signup models and authentication.

```python
@auth_namespace.route('/signup')
class SignUpAuth(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        '''
            SignUp authentication for new users
        '''
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = generate_password_hash(data['password'])

        new_user = Student(name=name, email=email, password=password)
        new_user.save()

        return new_user, HTTPStatus.CREATED
 ```

The above code will help the admin create a student account with the following credentials: email, name, and password.

<div style="font-size:15px; margin-top:10px; margin-bottom:20px;">
    The action code above will help admin in creating student account with the following credentials of: email, name and password.
</div>

# EndPoints For Student Management API

<div style="margin-top:8px; margin-bottom:10px; font-size:20px; font-weight:bold;">Auth EndPoint</div>
<!-- Tables for routing in each models -->

| ROUTE                    | METHOD | DESCRIPTION                                     | AUTHORIZATION          | USER TYPE |
| ------------------------ | ------ | ----------------------------------------------- | ---------------------- | --------- |
| `/api/auth/signup`       | _POST_ | Creation of students account                    | `None`                 | Any       |
| `/api/auth/login`        | _POST_ | Creation of JWT Tokens for students             | `None`                 | Students  |
| `/api/auth/refresh`      | _POST_ | Creation of Refresh Tokens for students account | `Bearer Refresh-Token` | Students  |
| `/api/auth/getme`        | _GET_  | Get Student Info                                | `Bearer Access-Token`  | Students  |
| `/api/auth/logout`       | _POST_ | LogOut User                                     | `Bearer Access-Token`  | Any       |
| `/api/auth/admin/signup` | _POST_ | Creation of Admin account                       | `None`                 | Admin     |
| `/api/auth/admin/login`  | _POST_ | Creation of JWT Tokens for Admin                | `None`                 | Admin     |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Admin EndPoint</div>

| ROUTE                                             | METHOD   | DESCRIPTION                           | AUTHORIZATION         | USER TYPE |
| ------------------------------------------------- | -------- | ------------------------------------- | --------------------- | --------- |
| `/api/admin/delete/<int:id>`                      | _DELETE_ | Delete Student by id                  | `Bearer Access-Token` | Admin     |
| `/api/admin/student/<int:student_id>/course`      | _DELETE_ | Delete Course for a Student By Admin  | `Bearer Access-Token` | Admin     |
| `/api/admin/course/<string:course_name>/students` | _GET_    | Get student registered in each course | `Bearer Access-Token` | Admin     |
| `/api/getallstudent`                              | _GET_    | Get all students                      | `Bearer Access-Token` | Admin     |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Student EndPoint</div>

| ROUTE                                                    | METHOD | DESCRIPTION                           | AUTHORIZATION         | USER TYPE |
| -------------------------------------------------------- | ------ | ------------------------------------- | --------------------- | --------- |
| `/api/update/me`                                         | _PUT_  | Update Student Info                   | `Bearer Access-Token` | Student   |
| `/api/auth/admin/grading/grade/student/<int:student_id>` | _POST_ | Grade Students By Id                  | `Bearer Access-Token` | Admin     |
| `/api/auth/admin/grading/grade/student`                  | _GET_  | Get Grades of Students by the student | `Bearer Access-Token` | Student   |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Course EndPoint</div>

| ROUTE                          | METHOD | DESCRIPTION             | AUTHORIZATION         | USER TYPE |
| ------------------------------ | ------ | ----------------------- | --------------------- | --------- |
| `/api/course/getall_course`    | _GET_  | Get all Course          | `Bearer Access-Token` | Any       |
| `/api/course/getme/get_course` | _GET_  | Get course of a Student | `Bearer Access-Token` | Student   |
| `/api/course/set_course`       | _POST_ | Register a Course       | `Bearer Access-Token` | Student   |
