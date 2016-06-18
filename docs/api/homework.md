## Create a Homework
Key      | Value
-------- | --------
URI      | /api/homework/
Method   | POST
Notes    | This API accepts five different types of objects in data. It will return the objects in the same order.

    /api/homework/ handles multiple operations
        which can be mixed and matched in the same request
        
    1. Create a new Homework
        No "id" is present; no "course_id" or "class_id" are present
    2. Create a new Homework and associate it to a previously created Course
        No "id" is present; a "course_id" is present
    3. Create a new Homework and associate it to a previously created Class
        No "id" is present; a "class_id" is present
    4. Associate a previously created Homework with a previously created Course
        An "id" is present; a "course_id" is present
    5. Associate a previously created Homework with a previously created Class
        An "id" is present; a "class_id" is present

The example payload contains these in order.

Request:

    {
        "data": [
            {
               "name": "Python Metaclasses"
            },
            {
               "name": "Python variables", "course_id": 1
            },
            {
               "name": "Python loops", "class_id": 10
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
            "len": 1,
        }
        "data": [
            {
               "id": 1,
               "name": "Python Metaclasses"
            },
            {
               "id": 2,
               "name": "Python variables",
               "course_homework_id": 500,
               "course_id": 1
            },
            {
               "id": 3,
               "name": "Python loops",
               "class_homework_id": 1001,
               "class_id": 10
            },
            {
               "id": 1,
               "course_homework_id": 501,
               "course_id": 1,
               "name": ""
            },
            {
               "id": 1,
               "class_homework_id": 1002,
               "class_id": 10,
               "name": ""
            },
        ]
    }

Note how the response returns the object in the exact order of the Response. You may use this guarentee to assign the front end objects their proper primary keys, for example.

Now how the 4th and 5th object contain the `course_homework_id` and `class_homework_id`, respectively. That would probably be necessary to add into the front end objects.
Also, these have an empty `name` attribute. That is because the backend isn't going to query the DB for them.


## Get a Homework
Key      | Value
-------- | --------
URI      | /api/homework/{id}/
Method   | GET
Query Params | ?data=course,class
Note     | To optionally include any of the associated Courses or Classes with this Homework, include the query parameters.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            "name": "Python Metaclasses",
            "parent_id": "",
            "classes": [
                {
                    "id": 1,
                    "name": "Python 2017",
                    "start_dt": "2017-01-01 00:00:00",
                    "end_dt": "2017-05-31 00:00:00",
                    "course_id": 1,
                    "class_homework_id": 1
                },
                ...
            ],
            "courses": [
                {
                    "id": 1,
                    "name": "Python",
                    "course_homework_id": 1
                },
                ...
            ]
        }
    }

## Get all Homeworks
Key      | Value
-------- | --------
URI      | /api/homework/
Query Params | ?course_id=1
Query Params | ?class_id=1
Method   | GET
Notes:   | Optionally include `?course_id=1` or `?class_id=1` to filter by `course_id` or `class_id`, but not both. If you add `?class_id=1` or `?course_id=1`, each of the objects will have a `class_homework_id` or `course_homework_id` added, respectively. This doesn't accept data query parameters. Should it?

Response:

    {
        "meta": {
            "len": 1
        },
        "data": [
            {
                "id": 1,
                "name": "Python Metaclasses",
                "parent_id": ""
                "course_homework_id": 1,
            },
            ...
        ]
    }


## Update a Homework

** TENTATIVELY IMPLEMENTED - PLEASE READ **

Key      | Value
-------- | --------
URI      | /api/homework/
Method   | PUT

This is somewhat hardcore, is the tentative design, and is subject to change.

Remember that a Homework can be associated at the Course level and the Class level. There are two cases:

Case | Description
-----|------------
1    | An admin ought to be able to alter the Homework at the Course level and have that propagate down to all Classes.
2    | A teacher on the other hand ought to be able to alter the Homework just for one particular class.

The goal of this API design is to accommodate both.

A quick note on Case 2: When a teacher "updates a Class level Homework", what actually happens in the backend is the following, if performed for the very **first** time:

1. A new Homework is created with all the same attributes as the Parent Homework
2. The new Homework's attributes are updated with whatever values are PUT in the object
3. The Class Homework associated to the old Homework is then associated with the new Homework

If the teacher decides to update the same Homework **again**, this doesn't happen, but rather the Homework object is updated directly. Note that the implementation for this relies on checking if parent_id is null, which is fine for the beta design but once we implement the Admin and Teacher template system this will need to change.

When the front end wants to update a Course level Homework (Case 1), the object passed in should contain the `id` of the Homework object and the Homework related attributes to change. It should NOT contain a `class_homework_id`.
When the front end wants to update a Class level Homework (Case 2), the object passed in should contain the `class_homework_id` of the ClassHomework object and the Homework related attributes to change. It should NOT contain a `id`

I think these two rules will be most subject to change. Perhaps it would make more sense in case 1 to name id `homework_id` or even `course_homework_id` and to prevent the use of `id` all together to avoid any confusion.

In the following example, the `data` array contains a Course level Homework (Case 1) to change and a Class level Homework (Case 2) to change, in that order

Request:

    {
        "data": [
            {
                "id": 1,
                "name": "Why Java > Python LOL JK"
            },{
                "class_homework_id": 1,
                "name": "Why Python > Java"
            }
        ]
    }

Note that the response is **much different** than PUTs on other models. Because in the Case 2 (Class level Homework change) update, we actually insert a new Homework object and then
mutate the ClassHomework's `homework_id` to the new Homework's `id`, this should be passed back to the front end who needs to update the front end objects accordingly. Note how the second object in this response has an `id`-- this
is the new Homework's `id`. The front end should update this.

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
                "class_homework_id": 1,
                "id": 4,
                "name": "Why Python > Java"
            }
        ]
    }

## Delete a Homework

** NOT IMPLEMENTED YET **

Key      | Value
-------- | --------
URI      | /api/homework/
Method   | DELETE
Notes    | This API accepts five different types of objects in `data` to cover the following three cases.

    1. Delete a new Homework
        "id" is present; no "course_id" or "class_id" are present
    2. Delete the association between a Homework and a Course
        A: "course_homework_id" is present 
        OR 
        B: "id AND "course_id" are present
    3. Delete the association between a Homework and a Class
        A: "class_homework_id" is present 
        OR 
        B: "id" AND "class_id" are present

Note that for case 2 and 3, the front end should always have `course_homework_id` and `class_homework_id` available.
This is a more efficient way of deleting the association because it involves one less call to the database.
I might disable the "id and course_id/class_id" combinations because of this.

Request:

    {
        "data": [
            {
                "id": 1,
            },
            {
                "id": 2, 
                "course_id": 1
            },
            {
                "id": 3,
                "course_id": 1
            },
            ...
        ]
    }

Response:

    {
        "meta": {
            "num_deleted": 3
        },
        "data": {}
    }


