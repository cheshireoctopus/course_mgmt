# Course


-------- | --------
heelo | goodbai

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


## Create a Class and add to a Course
