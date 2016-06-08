## Create a Student
Key      | Value
-------- | --------
URI      | /api/course/
Method   | POST
Notes    | This API accepts two different types of objects in data.

    /api/student has multiple operations, which can be mixed and matched in the same request
    1. Create a new Student
        No "id" is present; no "class_id" is present
    2. Create a new Student and associate it to a previously created Class
        No "id" is present; a "class_id" is present
    3. Associate a previously created Student with a previously created Class
        An "id" is present; a "class_id" is present

Request:

    {
        "data": [
            {
                "first_name": "Matthew",
                "last_name": "Moisen",
                "github_username": "mkmoisen",
                "email": "student@gmail.com",
                "photo_url": "http://www.matthewmoisen.com",
            },
            {
                "class_id": 1,
                "first_name": "Chandler",
                "last_name": "Moisen",
                "github_username": "cheshireoctopus",
                "email": "student@gmail.com",
                "photo_url": "http://www.chandlermoisen.com",
            },
            {
                "id": 1,
                "class_id": 1
            }
        ]
    }


Response:

    {
        "meta": {
            "len": 3
        },
        "data": [
            {
                "id": 2,
                "first_name": "Matthew",
                "last_name": "Moisen",
                "github_username": "mkmoisen",
                "email": "student@gmail.com",
                "photo_url": "http://www.matthewmoisen.com",
            },
            {
                "id": 3,
                "class_id": 1,
                "first_name": "Chandler",
                "last_name": "Moisen",
                "github_username": "cheshireoctopus",
                "email": "student@gmail.com",
                "photo_url": "http://www.chandlermoisen.com",
            },
            {
                "id": 1,
                "class_id": 1,
                "first_name": "",
                "last_name": "",
                "github_username": "",
                "email": "",
                "photo_url": ""
            }
        ]
    }

Note how the response returns the object in the exact order of the Response. You may use this guarantee to assign the front end objects their proper primary keys, for example.

Now how the 3rd object has empty attributes. That is because the backend isn't going to query the DB for them.


## Get a Student
Key      | Value
-------- | --------
URI      | /api/student/{id}
Method   | GET
Query Params | ?data=class,assignment,attendance
Note     | Do not follow up with a trailing slash. To optionally include any of the associated Classes, Assignments, or Attendances with this Student, include the query parameters.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "email": "student@gmail.com",
            "first_name": "Matthew",
            "last_name": "Moisen",
            "github_username": "mkmoisen",
            "photo_url": "http://www.matthewmoisen.com/"
            "assignments": [
                {
                    "class_homework_id": 1,
                    "class_student_id": 1,
                    "homework": {
                        "id": 1,
                        "name": "Python Metaclasses",
                        "parent_id": ""
                    },
                    "id": 1,
                    "is_completed": false
                },
                ...
            ],
            "attendances": [
                {
                    "class_lecture_id": 1,
                    "class_student_id": 1,
                    "did_attend": false,
                    "id": 1,
                    "lecture": {
                        "description": "Python Metaclasses Lecture",
                        "id": 1,
                        "name": "lecture1"
                    }
                },
                ...
            ],
            "classes": [
                {
                    "class_student_id": 1,
                    "course_id": 1,
                    "end_dt": "2015-06-01 00:00:00",
                    "id": 1,
                    "name": "Python 2016",
                    "start_dt": "2015-01-01 00:00:00"
                }
            ],

        }
    }



## Get all Students
Key      | Value
-------- | --------
URI      | /api/student/
Method   | GET
Query Params | ?class_id=1
Notes:   | Optionally include `?class_id=1` to filter by class_id. If you add `?class_id=1`, the objects will contain a `class_student_id`. This doesn't accept data query parameters. Should it?

Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
                "id": 1,
                "first_name": "Matthew",
                "last_name": "Moisen",
                "github_username": "mkmoisen",
                "email": "student@gmail.com",
                "photo_url": "http://www.matthewmoisen.com",
            },
            ...
        ]
    }


## Update a student

** NOT IMPLEMENTED **

Key      | Value
-------- | --------
URI      | /api/student/{id}
Method   | PUT
Note     | Do not follow up with a trailing slash

This example payload leaves out the `course_id`.
Payload:

    {
        "data": [
            {
                "id": 1,
                "name": "Why Java > Python LOL JK"
            }
        ]
    }

Response:

    {
        "meta": {},
        "data": {}
    }

## Delete a student

** NOT IMPLEMENTED YET **

Key      | Value
-------- | --------
URI      | /api/student/{id}
Method   | DELETE

Response:

    {
        "meta": {},
        "data": {}
    }


