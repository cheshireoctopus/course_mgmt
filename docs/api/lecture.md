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
URI      | /api/lecture/{id}/
Method   | GET
Query Params | ?data=course,class
Note     | To optionally include any of the associated Courses or Classes with this Homework, include the query parameters.

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

## Update a Lecture

** TENTATIVELY IMPLEMENTED - PLEASE READ **

Key      | Value
-------- | --------
URI      | /api/lecture/
Method   | PUT

This is somewhat hardcore, is the tentative design, and is subject to change.

Remember that a Lecture can be associated at the Course level and the Class level. There are two cases:

Case | Description
-----|------------
1    | An admin ought to be able to alter the Lecture at the Course level and have that propagate down to all Classes.
2    | A teacher on the other hand ought to be able to alter the Lecture just for one particular class.

The goal of this API design is to accommodate both.

A quick note on Case 2: When a teacher "updates a Class level Lecture", what actually happens in the backend is the following, if performed for the very **first** time:

1. A new Lecture is created with all the same attributes as the Parent Lecture
2. The new Lecture's attributes are updated with whatever values are PUT in the object
3. The Class Lecture associated to the old Lecture is then associated with the new Lecture

If the teacher decides to update the same lecture **again**, this doesn't happen, but rather the Lecture object is updated directly. Note that the implementation for this relies on checking if parent_id is null, which is fine for the beta design but once we implement the Admin and Teacher template system this will need to change.

When the front end wants to update a Course level Lecture (Case 1), the object passed in should contain the `id` of the Lecture object and the Lecture related attributes to change. It should NOT contain a `class_lecture_id`.
When the front end wants to update a Class level Lecture (Case 2), the object passed in should contain the `class_lecture_id` of the ClassLecture object and the Lecture related attributes to change. It should NOT contain a `id`

I think these two rules will be most subject to change. Perhaps it would make more sense in case 1 to name id `lecture_id` or even `course_lecture_id` and to prevent the use of `id` all together to avoid any confusion.

In the following example, the `data` array contains a Course level Lecture (Case 1) to change and a Class level Lecture (Case 2) to change, in that order

Request:

    {
        "data": [
            {
                "id": 1,
                "name": "Why Java > Python LOL JK"
            },{
                "class_lecture_id": 1,
                "name": "Why Python > Java"
            }
        ]
    }

Note that the response is **much different** than PUTs on other models. Because in the Case 2 (Class level Lecture change) update, we actually insert a new Lecture object and then
mutate the ClassLecture's `lecture_id` to the new Lecture's `id`, this should be passed back to the front end who needs to update the front end objects accordingly. Note how the second object in this response has an `id`-- this
is the new Lecture's `id`. The front end should update this.

Response:

    {
        "meta": {
            "len": 2
        },
        "data": [
            {
                "id": 1,
                "name": "Why Java > Python LOL JK"
            },
            {
                "class_lecture_id": 1,
                "id": 4,
                "name": "Why Python > Java"
            }
        ]
    }

## Delete a lecture

** NOT IMPLEMENTED YET **

Key      | Value
-------- | --------
URI      | /api/lecture/
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


