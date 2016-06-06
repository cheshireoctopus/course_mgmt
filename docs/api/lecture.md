# lecture

## Create a lecture
Key      | Value
-------- | --------
URI      | /api/lecture/
Method   | POST
Notes    | A Lecture can be created AND assocaited to a Course, or created independently, depending on whether a `course_id` is provided. The following payload shows them combined.
Payload:

    {
        "data": [
            {
                "name": "Why Python > Java",
                "description": "Python is so much greater than Java"
                "dt": "2016-01-01 00:00:00",
                "course_id": 1
            },
            {
                "name": Why Python > Node",
                "description": "Python is so much greater than Node"
                "dt": "2016-01-01",
            }
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
               "description": "Python is so much greater than Java",
               "dt": "2016-01-01 00:00:00
            },
            ...
        ]
    }

Note that the response will not include the course_id. Should it?

## Get a lecture
Key      | Value
-------- | --------
URI      | /api/lecture/{id}
Method   | GET
Note     | Do not follow up with a trailing slash

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Why Python > Java",
            "description": "Python is so much greater than Java",
            "dt": "2016-01-01 00:00:00"
        }
    }

## Get all lecturees
Key      | Value
-------- | --------
URI      | /api/lecture/
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
                "description": "Python is so much greater than Java",
                "dt": "2016-01-01 00:00:00"
            },{
                "id": 2,
                "name": Why Python > Node",
                "description": "Python is so much greater than Node"
                "dt": "2016-01-01",
            }
        ]
    }

## Update a lecture
Key      | Value
-------- | --------
URI      | /api/lecture/{id}
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

## Delete a lecture
** NOT IMPLEMENTED YET **
Key      | Value
-------- | --------
URI      | /api/lecture/{id}
Method   | DELETE

Response:

    {
        "meta": {},
        "data": {}
    }


## Get all Homework belonging to a lecture's Course
Key      | Value
-------- | --------
URI      | /api/lecture/{id}/homework/
Method   | DELETE

It is less expensive to use the [Course API](course.md) for this. Remember that a Homework is associated with
a Course and are global across lecturees. Assignments are `CourseHomeworks` that have been associated with `lectureStudents`.

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
                    "name": "Metalecturees
                },
                "course_homework": {
                    "course_id": 1,
                    "homework_id": 1
                }
            },
            ...
        ]
    }

## Get all Lectures belonging to a lecture

## Get all Assignments belonging to a lecture

## Get all Attendance belonging to a lecture

## Create a Lecture and assign to a lecture

## Create a Student and assign to a lecture

