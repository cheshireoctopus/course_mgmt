# Course

## Create a Course
Key      | Value
-------- | --------
URI      | /api/course/
Method   | POST
Notes    | This will return the objects with their primary keys
Payload:

    {
        "data": [
            {
                "name": "Python 101"
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
               "name": "Python 101"
            },
            ...
        ]
    }

## Get a Course
Key      | Value
-------- | --------
URI      | /api/course/{id}/
Method   | GET
Query Params | ?data=homework,lecture,class
Note     | To optionally include the corresponding Classes, Homework, and Lectures for this Course, use the query params as above.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Python 101",
            "classes": [
                {
                    "course_id": 1,
                    "id": 1,
                    "start_dt": "2017-01-01 00:00:00",
                    "end_dt": "2017-05-31 00:00:00"
                }
            ],
            "homeworks": [
                {
                    "id": 1,
                    "course_homework_id": 1,
                    "name": "Why Python > Java",
                    "parent_id": ""
                }
            ],
            "lectures": [
                {
                    "id": 1,
                    "course_lecture_id": 1,
                    "description": "The first lecture",
                    "name": "Lecture 1"
                }
            ]
        }
    }

## Get all Courses
Key      | Value
-------- | --------
URI      | /api/course/
Method   | GET
Query Params | ?data=homework,lecture,class
Notes    | This shouldn't support the query params like in the previous api, but its activated for the beta. This needs to be deactivated in the future, however. If there are 100 courses with 100 classes, 100 lectures, and 100 homeworks each, this will be really bad.

Response:

    {
        "meta": {
            "len": 2
        },
        "data": [
            {
                "id": 1,
                "name": "Python 101"
            },{
                "id": 2,
                "name": "Flask 101"
            }
        ]
    }

## Update a Course


Key      | Value
-------- | --------
URI      | /api/course/
Method   | PUT
Note     | Make sure to include the primary key

Payload:

    {
        "data": [
            {
                "id": 1,
                "name": "Javascript 101"
            }
        ]
    }

Response:

    {
        "meta": {},
        "data": {}
    }

Should I include anything in the response?

## Delete a Course

Key      | Value
-------- | --------
URI      | /api/course/
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
