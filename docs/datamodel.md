# Data Model

Here is an ERD of the database, created with [asciiflow](asciiflow.com). 
This ERD only list the Foreign Keys. 
The many side of a relationship is specified with an arrow.

                       +-------------+
                       |  Homework   |
                       +-------------+
            +----------+             +-----------+
            |          +-------------+           |
            |                                    |
    +-------v-------+                   +--------v-------+    +-------------------+
    |CourseHomework |                   | ClassHomework  |    |   Assignment      |
    +---------------+                   +----------------+    +-------------------+
    | homework_id   |                   | homework_id    +----> class_homework_id |
    | class_id      |                   | class_id       |    | class_student_id  |
    +-------^-------+                   +--------^-------+    +--------^----------+
            |                                    |                     |
            |                                    |                     |
            |                                    |            +--------+----------+
    +-------+-------+                   +--------+-------+    |   ClassStudent    |    +----------------+
    |     Course    |                   |    Class       |    +-------------------+    |    Student     |
    +---------------+                   +----------------+    | class_id          |    +----------------+
    |               +-------------------> course_id      +----> student_id        <----+                |
    +-------+-------+                   +--------+-------+    +--------+----------+    +----------------+
            |                                    |                     |
            |                                    |                     |
            |                                    |                     |
    +-------v-------+                   +--------v-------+    +--------v----------+
    | CourseLecture |                   |  ClassLecture  |    |     Attendance    |
    +---------------+                   +----------------+    +-------------------+
    | lecture_id    |                   | lecture_id     +---->  class_lecture_id |
    | course_id     |                   | class_id       |    |  class_student_id |
    +-------^-------+                   +--------^-------+    +-------------------+
            |                                    |
            |         +----------------+         |
            |         |    Lecture     |         |
            |         +----------------+         |
            +---------+                +---------+
                      +----------------+


