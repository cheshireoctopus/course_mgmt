#Overview

The API uses the following patterns:


## Headers
All of the APIs calls should use the following headers. The request must always be in JSON as will the response.

Key         |  Value
------------|--------
Content-Type| application/json
Accept      | application/json


## Trailing slash
Always include a trailing slash on all of the API calls.

Good    |  Bad
--------|-------
/api/class/ | /api/class
/api/class/1/ | /api/class/1
/api/class/1/?data=homework | /api/class/1?data=homework


## Create a {Model}
Key      | Value
-------- | --------
URI      | /api/{model}/
Method   | POST

For every `POST`, the API mandates that an array of objects be passed inside of the `data` attribute.
After creating the objects, the API will return these objects in the same order as passed in the request
and the primary keys will be in the objects as `id`. The front-end can take advantage of this ordered
guarantee to assign all of the front end objects the correct primary keys.

Depending on the Model you are `POST`ing, you may also include any foreign keys and not include mandatory fields. 
A Homework has a `M:N` relationship with Course. To create a new Homework and associate it with a previously creeated 
Course in a single call, add the `course_id` in the object. To associate a previously created Homework with a previously
created Courser, include both the `id` of the homework and the `course_id` of the course in the object, and do not
include any of the mandatory course fields, such as `name`. You can mix and match any of these options in a `POST`.

Request:

    {
        "data": [
            { ... },
            { ... },
            ...
        ]
    }

Response:

    {
        "meta": {
            "len": 2
        },
        "data": [
            {
                "id": 1, ...
            },
            {
                "id": 2, ...
            },
            ...
        ]
    }
    
## Read one {Model}
Key     | Value
--------|---------
URI     | /api/{model}/id/
Method  | GET
Query Params | ?data={model2},{model3},{model4}

If you wish to read a single Model based on the primary key, you have the option of finding the related models by using
the query parameters. For example, to get a Single homework with a primary key `id` of 1 and all the related Courses,
call `/api/homework/1/?data=course` You can include 1 or more models using this syntax. The related models will exist
as an array containing objects of each related model. These objects will contain at least the primary key of the related
model object; if the related model is on the M:1 side, the foreign key to the model; if thre realted model is M:N,
the M:M table's primary key will be included as well.

Response:

    {
        "meta": {},
        "data": {
            "id": 1,
            ...,
            "{model2}s": [
                { "id": 1, ... },
                { "id": 2, ... },
                ...
            ],
            "{model3}s": [
                { "id": 1, ... },
                { "id": 2, ... }
            ]
        }
    }