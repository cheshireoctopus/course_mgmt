# Assignment

## Create a Assignment

** NOT SUPPORTED **

An assignment is created in one of these ways:

1. A Class is created. This instantiates all the Assignments from the associated ClassHomeworks (which are instantiated from the associated CourseHomeworks)
2. A Homework is created and associated to a Class in the same call. This instantiates the Assignment.


## Get one Assignment

Key      | Value
-------- | --------
URI      | /api/assignment/{id}/
Method   | GET
Query Params | 
Note     | This technically works, but it isn't customized like the other models. The normal access pattern is to get All assignments filtered by something, which is below

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "class_homework_id": 1,
            "class_student_id": 1
        }
    }

## Get all Assignments
Key      | Value
-------- | --------
URI      | /api/assignment/
Method   | GET
Query Params | ?class_homework_id=1
Query Params | ?class_student_id=1
Query Params | ?class_id=1
Query Params | ?student_id=1
Notes:   | To get all the assignments for a given `class_homework_id`, or `class_student_id`, or `class_id`, or `student_id` use the query params. Only one is permitted. This one is a bit different from most of the models in that it will return the associated models, because it is useless without it.

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

## Update an Assignment


Key      | Value
-------- | --------
URI      | /api/assignment/
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


## Delete an assignment

** NOT SUPPORTED **

An Assignment has no reason to be deleted directly. If one of these models are deleted, the assignment will be deleted:

1. Homework
2. ClassHomework
3. Class
4. ClassStudent
5. Student
