# Course

Key      | Value
-------- | --------
heelo | goodbai

## Create a Course
Key      | Value
-------- | --------
URI      | /api/course
Method   | POST
Payload:

    {
      "data": [
        {
          "name": {name}
        }
      ]
    }

Does it work | probably not

### PUT
    /api/course/
    {
      "data": [
        {
          "id": {id},
          "name": {name}
        }
      ]
    }
