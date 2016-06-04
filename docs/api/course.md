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
            "len": <int: length of items in data array>
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
URI      | /api/course/{id}
Method   | GET
Note     | Do not follow up with a trailing slash

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Python 101"
        }
    }

## Get all Courses
Key      | Value
-------- | --------
URI      | /api/course/
Method   | GET

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
URI      | /api/course/{id}
Method   | PUT
Note     | Do not follow up with a trailing slash

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

## Delete a Course
** NOT IMPLEMENTED YET **
Key      | Value
-------- | --------
URI      | /api/course/{id}
Method   | DELETE

Response:

    {
        "meta": {},
        "data": {}
    }

## Create a Class and add to a Course
**Not implemented yet**

Key      | Value
-------- | --------
URI      | /api/course/{id}/class/
Method   | POST
Note     | The same can be accomplished on [Class](class.md).

Payload:

    {
        "data": [
            {
                "name": "Why Python > Java"
            },{
                "name": "Why Python > JavaScript"
            }
        ]
    }

Response:

    {
        "data": [
            {
                "id": 1,
                "name": "Why Python > Java",
                "course_id": 1
            },{
                "id: 2,
                "name": "Why Python > JavaScript",
                "course_id": 1
            }
        ]
    }

## Get all Classes for a Course
Key      | Value
-------- | --------
URI      | /api/course/{id}/class/
Method   | GET

Response:

    {
        "meta": {
            "len": 2,
        },
        "data": [
            {
                "id": 1,
                "name": "Why Python > Java",
                "course_id": 1
            },{
                "id: 2,
                "name": "Why Python > JavaScript",
                "course_id": 1
            }
        ]
    }

## Add Homework to a Course
Key      | Value
-------- | --------
URI      | /api/course/{id}/homework/
Method   | POST
Note     | This can NOT be accomplished through [Homework](homework.md).

There are two options for this.

### Homework has already previously been created
We only want to associate the Homework with this course
Payload:

    {
        "data": [
            {
                "homework_id": 1
            },
            ...
        ]
    }

### Create Homework while simutaneously associating it with a Course
We want to create a homework and then add it
Payload:

    {
        "data": [
            {
                "name": "Metaclasses"
            },
            ...
        ]
    }

### The response is the same in either case:
Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
                "course_id": 1,
                "homework_id': 1
            },
            ...
        ]
    }

Note that you will NOT receive the Homework's attributes, other than the `id`.
If you want that, then create a Homework through the [Homework](homework.md) API.

## See all Homework for a Course
Key      | Value
-------- | --------
URI      | /api/course/{id}/homework/
Method   | GET
Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
                "id": 1,
                "name": "Metaclasses"
            }
        ]
    }

Note that just returns the Homework objects but NOT the associated CourseHomework IDs. Should it??