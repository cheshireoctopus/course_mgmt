# Class

## Create a Class
Key      | Value
-------- | --------
URI      | /api/class/
Method   | POST
Notes    | The same can be Accomplished in [/api/class/{id}/class/](class.md)
Payload:

    {
        "data": [
            {
                "name": "Why Python > Java",
                "course_id": 1
            },
            ...
        ]
    }

Response:

    {
        "meta": {
            "len": <int: length of items in data array>
        },
        "data": [
            {
               "id": 1,
               "name": "Why Python > Java",
               "course_id": 1
            },
            ...
        ]
    }

## Get a Class
Key      | Value
-------- | --------
URI      | /api/class/{id}
Method   | GET
Note     | Do not follow up with a trailing slash

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Why Python > Java",
            "course_id": 1
        }
    }

## Get all Classes
Key      | Value
-------- | --------
URI      | /api/class/
Method   | GET

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
URI      | /api/class/{id}
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

## Delete a class
** NOT IMPLEMENTED YET **
Key      | Value
-------- | --------
URI      | /api/class/{id}
Method   | DELETE

Response:

    {
        "meta": {},
        "data": {}
    }


## Get all Homework belonging to a Class's Course
Key      | Value
-------- | --------
URI      | /api/class/{id}/homework/
Method   | DELETE

It is less expensive to use the [Course API](course.md) for this. Remember that a Homework is associated with
a Course and are global across classes. Assignments are `CourseHomeworks` that have been associated with `ClassStudents`.

Note how this data array has an object containing both the Homework and the `CourseHomework` objects.

Response:

    {
        "meta": {
            "len": 2
        },
        "data": [
            {
                "homework": {
                    "id": 1,
                    "name": "Metaclasses
                },
                "course_homework": {
                    "course_id": 1,
                    "homework_id": 1
                }
            },
            ...
        ]
    }

## Get all Lectures belonging to a Class

## Get all Assignments belonging to a Class

## Get all Attendance belonging to a Class

## Create a Lecture and assign to a Class

## Create a Student and assign to a Class

