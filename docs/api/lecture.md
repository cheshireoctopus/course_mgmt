# lecture

## Create a lecture
Key      | Value
-------- | --------
URI      | /api/lecture/
Method   | POST
Notes    | This API accepts five different types of objects in data. It will return the objects in the same order.


    api/lecture/ handles multiple operations
        which can be mixed and matched in the same request
    1. Create a new Lecture
        No "id" is present; no "course_id" or "class_id" are present
    2. Create a new Lecture and associate it to a previously created Course
        No "id" is present; a "course_id" is present
    3. Create a new Lecture and associate it to a previously created Class
        No "id" is present; a "class_id" is present
    4. Associate a previously created Lecture with a previously created Course
        An "id" is present; a "course_id" is present
    5. Associate a previously created Lecture with a previously created Class
        An "id" is present; a "class_id" is present

Note that ClassLectures must have a "dt" attribute. Lectures associated to Courses do not have this.

Request:

    {
        "data": [
            {
               "name": "Python Metaclasses Lecture",
               "description": "Useful description"
            },
            {
               "name": "Python variables lecture",
               "description": "Useful description",
               "course_id": 1
            },
            {
               "name": "Python loops lecture",
               "description": "Useful description",
               "dt": "2017-01-01 00:00:00"
               "class_id": 10
            },
            {
               "id": 1, "course_id": 1
            },
            {
               "id": 1, "class_id": 10
            },
        ]
    }


Response:

    {
        "meta": {
            "len": 5
        }
        "data": [
            {
               "id": 1,
               "name": "Python Metaclasses Lecture",
               "description": "Useful description"
            },
            {
               "id": 2,
               "name": "Python variables lecture",
               "description": "Useful description",
               "course_lecture_id": 500,
               "course_id": 1
            },
            {
               "id": 3,
               "name": "Python loops lecture",
               "description": "Useful description",
               "dt": "2017-01-01 00:00:00"
               "class_lecture_id": 1001,
               "class_id": 10
            },
            {
               "id": 1,
               "course_lecture_id": 501,
               "course_id": 1,
               "name": ""
               "description": "",
            },
            {
               "id": 1,
               "class_lecture_id": 1002,
               "class_id": 10,
               "name": "",
               "dt": ""
            },
        ]
    }

Note how the response returns the object in the exact order of the Response. You may use this guarantee to assign the front end objects their proper primary keys, for example.

Now how the 4th and 5th object contain the `course_homework_id` and `class_homework_id`, respectively. That would probably be necessary to add into the front end objects.
Also, these have an empty `name` attribute. That is because the backend isn't going to query the DB for them.


## Get a Lecture
Key      | Value
-------- | --------
URI      | /api/lecture/{id}
Method   | GET
Query Params | ?data=course,class
Note     | Do not follow up with a trailing slash. To optionally include any of the associated Courses or Classes with this Homework, include the query parameters.

If you include `?data=class`, the objects in the `classes` dict will contain a `dt` attribute from the ClassLecture. Don't confuse this with the Class's `start_time` and `end_time`.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Python Metaclasses Lecture",
            "description": "A useful description"
            "parent_id": "",
            "classes": [
                {
                    "id": 1,
                    "name": "Python 2017",
                    "start_dt": "2017-01-01 00:00:00",
                    "end_dt": "2017-05-31 00:00:00",
                    "course_id": 1,
                    "class_lecture_id": 1
                },
                ...
            ],
            "courses": [
                {
                    "id": 1,
                    "name": "Python",
                    "course_lecture_id": 1
                },
                ...
            ]
        }
    }

## Get all Lectures
Key      | Value
-------- | --------
URI      | /api/lecture/
Query Params | ?course_id=1
Query Params | ?class_id=1
Method   | GET
Notes:   | Optionally include ?course_id=1 or ?class_id=1 to filter by course_id or class_id, but not both. If you add `?class_id=1` or `?course_id=1`, each of the objects will have a `class_lecture_id` or `course_lecture_id` added, respectively. This doesn't accept data query parameters. Should it?

If you include `?class_id=1`, the class objects will include the ClassLecture `dt` attribute.

Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
                "id": 1,
                "name": "Python Metaclasses Lecture",
                "description": "A useful description",
                "dt": "2017-01-01 00:00:00"
                "class_lecture_id": 1
            },
            ...
        ]
    }

## Update a lecture

** NOT IMPLEMENTED **

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


