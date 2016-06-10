# Attendance

## Create a Attendance

** NOT SUPPORTED **

An attendance is created in one of these ways:

1. A Class is created. This instantiates all the Attendances from the associated ClassLectures (which are instantiated from the associated CourseLectures)
2. A Lecture is created and associated to a Class in the same call. This instantiates the Attendance.


## Get one Attendance

Key      | Value
-------- | --------
URI      | /api/attendance/{id}/
Method   | GET
Query Params | 
Note     | This technically works, but it isn't customized like the other models. The normal access pattern is to get All attendances filtered by something, which is below

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "class_lecture_id": 1,
            "class_student_id": 1
        }
    }

## Get all Attendances
Key      | Value
-------- | --------
URI      | /api/attendance/
Method   | GET
Query Params | ?class_lecture_id=1
Query Params | ?class_student_id=1
Query Params | ?class_id=1
Query Params | ?student_id=1
Notes:   | To get all the attendances for a given `class_lecture_id`, or `class_student_id`, or `class_id`, or `student_id`, use the query params. Only one is permitted. This one is a bit different from most of the models in that it will return the associated models, because it is useless without it.

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

## Update an Attendance


Key      | Value
-------- | --------
URI      | /api/attendance/
Method   | PUT
Note     | 

Request:

    {
        "data": [
            {
                "id": 1,
                "did_complete": true
            }
        ]
    }

Response:

    {
        "meta": {},
        "data": {}
    }


## Delete an attendance

** NOT SUPPORTED **

An Attendance has no reason to be deleted directly. If one of these models are deleted, the attendance will be deleted:

1. Lecture
2. ClassLecture
3. Class
4. ClassStudent
5. Student
