# Class

## Create a Class
Key      | Value
-------- | --------
URI      | /api/class/
Method   | POST
Request:

    {
        "data": [
            {
                "name": "Spring 2016 Python 101",
                "course_id": 1,
                "start_dt": "2017-01-01 00:00:00",
                "end_dt": "2017-05-31 00:00:00"
            },
            ...
        ]
    }

Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
               "id": 1,
               "name": "Spring 2016 Python 101",
               "start_dt": "2017-01-01 00:00:00",
               "end_dt": "2017-05-31 00:00:00"
               "course_id": 1
            },
            ...
        ]
    }

## Get a Class
Key      | Value
-------- | --------
URI      | /api/class/{id}/
Method   | GET
Query Params | ?data=student,homework,lecture,course
Note     | To optionally include any of the associated Students, Homeworks, Lectures, or Course with this Class, include the query parameters.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "2017 Spring Python 101",
            "start_dt": "2017-01-01 00:00:00",
            "end_dt": "2017-05-31 00:00:00"
            "course_id": 1,
            "course": {
                "id": 1,
                "name": "Python 101"
            },
            "homeworks": [
                {
                    "id": 1,
                    "class_homework_id": 1,
                    "name": "Homework 1"
                    "parent_id": "",
                },
                ...
            ],
            "students": [
                {
                    "id": 1,
                    "class_student_id": 1,
                    "email": "student@gmail.com",
                    "first_name": "Matthew",
                    "last_name": "Moisen",
                    "github_username": "mkmoisen",
                    "photo_url": "http://www.matthewmoisen.com"
                },
                ...
            ],
            "lectures": [
                {
                    "id": 1,
                    "class_lecture_id": 1,
                    "description": "The first lecture",
                    "name": "Lecture 1"
                    "dt": "2017-01-01 00:00:00"
                },
                ...
            ]
        }
    }

## Get all Classes
Key      | Value
-------- | --------
URI      | /api/class/
Method   | GET
Query Params | ?course_id=1
Notes:   | To get all the classes for a given course id, use the query params. This doesn't accept `data` query parameters. Should it?

Response:

    {
        "meta": {
            "len": 2
        },
        "data": [
            {
                "id": 1,
                "name": "Why Python > Java",
                "course_id": 1
            },{
                "id": 2,
                "name": "Why Python > JavaScript",
                "course_id": 1
            }
        ]
    }

## Update a class

Key      | Value
-------- | --------
URI      | /api/class/
Method   | PUT
Note     | 

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


## Delete a class

Key      | Value
-------- | --------
URI      | /api/class/
Method   | DELETE

Request:

    {
        "data": [
            {
                "id": 1
            },
            ...
        ]
    }   

Response:

    {
        "meta": {
            "num_deleted": 1
        },
        "data": {}
    }
