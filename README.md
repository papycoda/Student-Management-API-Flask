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

admin_auth
Authentication for admin



# EndPoints For Student Management API

<div style="margin-top:8px; margin-bottom:10px; font-size:20px; font-weight:bold;">Auth EndPoint</div>
<!-- Tables for routing in each models -->
POST

/auth/admin/course/add_grade/int:course_id/int:student_id 

Add grade for a student in a course

DELETE       |   _/auth/admin/course/delete_grade/int:grade_id_  |  _Delete an existing grade_


PUT |    _/auth/admin/course/edit_grade/int:grade_id_ |    _Update an existing grade_

GET
/auth/admin/courses
Get all courses

POST
/auth/admin/courses
Add a new course

PUT
/auth/admin/courses
Update an existing course

DELETE
/auth/admin/courses
Delete an existing course

POST
/auth/admin/login
Authenticate Login for admin

POST
/auth/admin/signup
Authenticate Signup for admin




<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Admin EndPoint</div>
course
CRUD for courses with paths



POST

/course/create_course

Create Course

GET

/course/getall_course

Get all courses in database with Authorization

GET

/course/getme/get_course

Get courses for a user based on track using Authorization

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Student EndPoint</div>

Students
Authentication for student management api



GET

/Students/

Get All Students

POST

/Students/signup

Student Signup

GET

/Students/student/{id}

Get a specific student by ID

PUT

/Students/student/{id}

Update a specific student by ID

DELETE

/Students/student/{id}

Delete a specific student by ID


<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Course EndPoint</div>

GET

/admin/course/{course_name}/students

Get student registered in each course

DELETE

/admin/delete/{id}

Delete Student by id

DELETE

/admin/student/{student_id}/course

Delete Course for a Student By Admin


