__author__ = 'mmoisen'
from flask import Flask
from course_mgmt.models import *  # db, all_models
import unittest
import requests
from course_mgmt.views.api import extract_data, parse_data_from_query_args, parse_id_from_query_args, json_to_model
from course_mgmt.views.api import hardcore_update
import json
from sqlalchemy.orm.exc import NoResultFound
URL = 'http://localhost:5000'

class SqliteSequence(db.Model):
    __tablename__ = 'sqlite_sequence'
    name = db.Column(db.String, primary_key=True)
    seq = db.Column(db.Integer)

def get_first_id_from_response(r, id_key='id'):
    '''
    Utility method to pull the first ID from a response object
    Remember responses look like this:
        {
            "data": [
                { ... },
                { ...}
            ]
        }
    :param r: response object from requests
    :return: id
    '''
    return r.json()['data'][0][id_key]

def hit_api(api, data=None, params=None, method='POST'):
    '''
    Utility method to hit any of the APIs
    :param api: Full API after host:port
                /api/course/create/
    :param data: Dict containing the data to hit the API with
    :param method: 'POST', 'GET', 'PUT', 'DELETE'
    :return: a response object from requests
    '''
    r = getattr(requests, method.lower())(URL + api, json=data, params=params)
    return r

def drop_and_create_db():
    api = '/api/drop/'
    r = hit_api(api)

    # Change the starting sequences to try to find bugs in join conditions
    index = 1
    db.session.query(SqliteSequence).delete()
    for table in all_models:
        s = SqliteSequence(name=table.__tablename__, seq=index)
        db.session.add(s)
        index += 100

    db.session.commit()


    return r

class TestLol(unittest.TestCase):
    def test_lol(self):
        drop_and_create_db()

def create_course(name):
    '''
    Utility function to create a single course
    '''
    api = '/api/course/'
    method = 'POST'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_course(id, name):
    api = '/api/course/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_course(id):
    api = '/api/course/{}'.format(id)  # No trailing slashes on ID due to flask-classy constraint
    method = 'GET'
    return hit_api(api, method=method)

def create_class_lecture(class_id, name, description, dt):
    # Utility function to create a single lecture
    api = '/api/lecture/'
    method = 'POST'
    data = {
        'data': [
            {
                'class_id': class_id,
                'name': name,
                'description': description,
                'dt': dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_course_lecture(course_id, name, description):
    api = '/api/lecture/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name,
                'description': description,
            }
        ]
    }

    return hit_api(api, data, method=method)


def update_lecture(id, name, description, dt):
    # Utility function to create a single lecture
    api = '/api/lecture/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name,
                'description': description,
                'dt': dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_lecture(id):
    api = '/api/lecture/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)


def create_class(course_id, name, start_dt, end_dt):
    '''
    Utility function to create a single class
    '''
    api = '/api/class/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name,
                'start_dt': start_dt,
                'end_dt': end_dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_class(id, name, start_dt, end_dt):
    api = '/api/class/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'start_dt': start_dt,
                'end_dt': end_dt,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_class(id):
    api = '/api/class/{}'.format(id)
    method = 'GET'
    return hit_api(api, method=method)

def create_homework_independent(name):
    # Creates an indepenent homework
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_homework(id, name):
    api = '/api/homework/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_homework(id):
    api = '/api/homework/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)

def add_homework_independent_to_course(course_id, homework_id):
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'id': homework_id,
                'course_id': course_id
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_homework_dependent(course_id, name):
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'course_id': course_id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_class_homework(class_id, name):
    api = '/api/homework/'
    method = 'POST'
    data = {
        'data': [
            {
                'class_id': class_id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_student_independent(first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_student(id, first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'PUT'
    data = {
        'data': [
            {
                'id': id,
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

def get_student(id):
    api = '/api/student/{}'.format(id)
    method = 'GET'

    return hit_api(api, method=method)

def add_student_independent_to_class(class_id, student_id):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'id': student_id,
                'class_id': class_id
            }
        ]
    }

    return hit_api(api, data, method=method)

def create_student_dependent(class_id, first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
    method = 'POST'
    data = {
        'data': [
            {
                'class_id': class_id,
                'first_name': first_name,
                'last_name': last_name,
                'github_username': github_username,
                'email': email,
                'photo_url': photo_url
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_class_homework(class_homework_id, name):
    '''
    Used to update a homework that is associated to a class
    Which actually creates a new Homework row and mutates the ClassHomework row to point to the Homework row
    :param class_homework_id:
    :param name:
    :return:
    '''
    api = '/api/homework/'
    method = 'PUT'
    data = {
        'data': [
            {
                'class_homework_id': class_homework_id,
                'name': name
            }
        ]
    }

    return hit_api(api, data, method=method)

def update_class_lecture(class_lecture_id, name, description, dt):
    '''
    Used to update a lecture that is associated to a class
    Which actually creates a new Lecture row and mutates the ClassLecture row to point to the Lecture row
    :param class_lecture_id:
    :param name:
    :return:
    '''
    api = '/api/lecture/'
    method = 'PUT'
    data = {
        'data': [
            {
                'class_lecture_id': class_lecture_id,
                'name': name,
                'description': description,
                'dt': dt.strftime(date_format) if isinstance(dt, datetime) else dt
            }
        ]
    }

    return hit_api(api, data, method=method)

def delete_homework(homework_id):
    '''
    Used to delete a Homework
    '''
    api = '/api/homework/'
    method = 'DELETE'
    data = {
        'data': [
            {
                'id': homework_id
            }
        ]
    }

    return hit_api(api, data, method=method)

def delete_course_homework(id=None, course_id=None, course_homework_id=None):
    assert not id ^ course_id
    assert (id and course_id) ^ course_homework_id

    case_1 = True if id and course_id else False

    api = '/api/homework/'
    method = 'DELETE'
    data = {
        'data': [
            {'id': id, 'course_id': course_id} if case_1 else {'course_homework_id': course_homework_id}
        ]
    }

    return hit_api(api, data, method=method)

def delete_class_homework(id=None, class_id=None, class_homework_id=None):
    assert not id ^ class_id
    assert (id and class_id) ^ class_homework_id

    case_1 = True if id and class_id else False

    api = '/api/homework/'
    method = 'DELETE'
    data = {
        'data': [
            {'id': id, 'class_id': class_id} if case_1 else {'class_homework_id': class_homework_id}
        ]
    }

    return hti_api(api, data, method=method)

class TestAll(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

    def assert_data_equals(self, r, **kwargs):
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['data'], kwargs)

    def test_all_create(self):
        '''
        This system test hits all of the create APIs happy path
        The purpose of this is to quickly tell if anything major is broken
        :return:
        '''
        ## Create Course
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        # Get Course
        r = get_course(id=course_id)
        self.assert_data_equals(r, id=course_id, name='Matthew''s Course')
        #self.assertEquals(r.json()['name'], 'Matthew''s Course')

        ## Update Course

        r = update_course(id=course_id, name='Chandler''s Course')
        self.assertEquals(r.status_code, 200)

        # Get Course
        r = get_course(id=course_id)
        self.assert_data_equals(r, id=course_id, name='Chandler''s Course')

        ## Create Class
        r = create_class(course_id=course_id, name='Spring 2016', start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        # Get Class
        r = get_class(class_id)
        self.assert_data_equals(r, id=class_id, name='Spring 2016', start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00',
                                course_id=course_id)

        ## Update Class
        r = update_class(id=class_id, name='Spring 2015', start_dt='2015-01-01 00:00:00', end_dt='2015-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        # Get Class
        r = get_class(class_id)
        self.assert_data_equals(r, id=class_id, name='Spring 2015', start_dt='2015-01-01 00:00:00', end_dt='2015-05-30 00:00:00', course_id=course_id)


        #r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        #self.assertEquals(r.status_code, 200)

        ## Create Course Lecture
        r = create_course_lecture(course_id=course_id, name='Lecture 1', description='The first lecture1')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        # Get Lecture
        r = get_lecture(lecture_id)
        self.assert_data_equals(r, id=lecture_id, name='Lecture 1', description='The first lecture1', parent_id='')

        # Update lecture
        #r = update_lecture(id=lecture_id, name='Lecture 2', description='The second lecture', dt='2015-01-01 00:00:00')
        #self.assertEquals(r.status_code, 200)

        # Get Lecture
        #r = get_lecture(lecture_id)
        #self.assert_data_equals(r, id=lecture_id, class_id=class_id, name='Lecture 2', description='The second lecture', dt='2015-01-01 00:00:00')

        ## Create Independent Homework and add to Course
        # Create Independent Homework
        r = create_homework_independent(name='Homework 1')
        self.assertEquals(r.status_code, 200)

        homework_independent_id = get_first_id_from_response(r)

        # Get Homework
        r = get_homework(homework_independent_id)
        # Shouldn't parent id be null not empty string
        self.assert_data_equals(r, parent_id='', id=homework_independent_id, name='Homework 1')

        # Update homework
        #r = update_homework(id=homework_independent_id, name='Homework 2')
        #self.assertEquals(r.status_code, 200)

        # Get Homework
        #r = get_homework(homework_independent_id)
        #self.assert_data_equals(r, parent_id='', id=homework_independent_id, name='Homework 2')

        # Add independent homework to Course
        r = add_homework_independent_to_course(course_id=course_id, homework_id=homework_independent_id)
        self.assertEquals(r.status_code, 200)

        course_homework_id_1 = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 2')
        self.assertEquals(r.status_code, 200)
        course_homework_id_2 = get_first_id_from_response(r)

        ## Create Independent Student and Add to Class
        # Create Independent Student
        r = create_student_independent(first_name='Matthew', last_name='Moisen', github_username='mkmoisen',
                                       email='mkmoisen@gmail.com', photo_url='http://matthewmoisen.com/pic.jpg')

        self.assertEquals(r.status_code, 200)

        student_independent_id = get_first_id_from_response(r)

        # Get Student
        r = get_student(student_independent_id)
        self.assert_data_equals(r, id=student_independent_id, first_name='Matthew', last_name='Moisen',
                                github_username='mkmoisen', email='mkmoisen@gmail.com',
                                photo_url='http://matthewmoisen.com/pic.jpg')

        # Update Student
        r = update_student(id=student_independent_id, first_name='Chandler', last_name='Moisen', github_username='ches',
                           email='hello@chandlermoisen.com', photo_url='http://chandlermoisen.com/pic/jpg')
        self.assertEquals(r.status_code, 200)

        # Get Student
        r = get_student(student_independent_id)
        self.assert_data_equals(r, id=student_independent_id, first_name='Chandler', last_name='Moisen',
                                github_username='ches', email='hello@chandlermoisen.com',
                                photo_url='http://chandlermoisen.com/pic/jpg')

        # Add Independent Student to Class
        r = add_student_independent_to_class(class_id, student_independent_id)
        self.assertEquals(r.status_code, 200)

        class_student_id_1 = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id_2 = get_first_id_from_response(r)


def create_interference():
    '''
    Create a completely different course/class/lecture/homework/student to see if it interferes
    '''

    course = Course(name='Interference Course')
    db.session.add(course)
    db.session.flush()

    lecture = Lecture(name='Interference Lecture', description='The first interference')
    db.session.add(lecture)
    db.session.flush()

    course_lecture = CourseLecture(course_id=course.id, lecture_id=lecture.id)
    db.session.add(course_lecture)

    homework = Homework(name='Interference Hmk')
    db.session.add(homework)
    db.session.flush()

    course_homework = CourseHomework(course_id=course.id, homework_id=homework.id)
    db.session.add(course_homework)

    clazz = Class(course_id=course.id, name='Interference 2015', start_dt=datetime.now(), end_dt=datetime.now())
    db.session.add(clazz)
    db.session.flush()

    class_homework = ClassHomework(class_id=clazz.id, homework_id=homework.id)
    db.session.add(class_homework)
    db.session.flush()

    class_lecture = ClassLecture(class_id=clazz.id, lecture_id=lecture.id, dt=datetime.now())
    db.session.add(class_lecture)
    db.session.flush()

    student = Student(first_name='Inter', last_name='Ference', github_username='interference',
                                 email='inter@ference.com', photo_url='http://interference.com/pic.jpg')
    db.session.add(student)
    db.session.flush()

    class_student = ClassStudent(class_id=clazz.id, student_id=student.id)
    db.session.add(class_student)
    db.session.flush()

    attendance = Attendance(class_student_id=class_student.id, class_lecture_id=class_lecture.id)
    db.session.add(attendance)

    assignment = Assignment(class_student_id=class_student.id, class_homework_id=class_homework.id)
    db.session.add(assignment)
    db.session.commit()



class TestPutHomework(unittest.TestCase):
    def setUp(self):


        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)
        create_interference()
        course = Course(name="Matthew")
        db.session.add(course)
        #db.session.flush()

        homework = Homework(name="Homework 1")
        db.session.add(homework)
        db.session.flush()

        self.original_homework_id = homework.id

        course_homework = CourseHomework(course_id=course.id, homework_id=homework.id)
        db.session.add(course_homework)

        clazz = Class(course_id=course.id, name="Matthew 2016", start_dt=datetime.now(), end_dt=datetime.now())
        db.session.add(clazz)
        db.session.flush()

        class_homework = ClassHomework(class_id=clazz.id, homework_id=homework.id)
        db.session.add(class_homework)
        db.session.flush()
        db.session.commit()

        self.class_homework_id = class_homework.id



    def assert_homework_first_update(self):
        q = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.id==self.class_homework_id)
        homework, class_homework = q.one()

        self.assertEquals(homework.name, 'Homework 100')
        self.assertEquals(homework.parent_id, self.original_homework_id)

        # If I dont delete thsese, the next query down below gets stale data for some reason -- why does this happen?
        del homework
        del class_homework

        original_homework = db.session.query(Homework).filter_by(id=self.original_homework_id).one()
        self.assertEquals(original_homework.id, self.original_homework_id)

    def assert_homework_second_update(self):

        ## Update the class homework for the second time


        print "class_homework_id is ", self.class_homework_id
        q = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.id==self.class_homework_id)
        homework, class_homework = q.one()
        self.assertEquals(homework.name, 'Homework 1000')
        self.assertEquals(homework.parent_id, self.original_homework_id)

    def test_rest_update_homework(self):
        '''
        This is when a teacher "updates" a class homework for the first time
            which actually creates a new Homework using the old Course Homework, makes the changes
            and switches the homework_id in ClassHomework to point to the new homework
        '''

        # Update the class homework for the very first time
        r = update_class_homework(class_homework_id=self.class_homework_id, name='Homework 100')
        self.assertEquals(r.status_code, 200)
        # Todo: check data response

        self.assert_homework_first_update()

        r = update_class_homework(class_homework_id=self.class_homework_id, name='Homework 1000')
        self.assertEquals(r.status_code, 200)

        self.assert_homework_second_update()

    def test_function_update_homework(self):
        app = Flask(__name__)
        data = {
            'data': [
                {
                    'class_homework_id': self.class_homework_id,
                    'name': 'Homework 100'
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # First update
        with app.test_request_context(headers=headers, data=json.dumps(data)):
            r = hardcore_update(Homework)
            self.assertEquals(r[1], 200)
            # Todo: check data response

            self.assert_homework_first_update()

        data['data'][0]['name'] = 'Homework 1000'

        #Second update
        with app.test_request_context(headers=headers, data=json.dumps(data)):
            r = hardcore_update(Homework)
            self.assertEquals(r[1], 200)

            self.assert_homework_second_update()


class TestPutLecture(unittest.TestCase):
    def setUp(self):


        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)
        create_interference()
        course = Course(name="Matthew")
        db.session.add(course)
        #db.session.flush()

        lecture = Lecture(name="Lecture 1", description='Description 1')
        db.session.add(lecture)
        db.session.flush()

        self.original_lecture_id = lecture.id

        course_lecture = CourseLecture(course_id=course.id, lecture_id=lecture.id)
        db.session.add(course_lecture)

        clazz = Class(course_id=course.id, name="Matthew 2016", start_dt=datetime.now(), end_dt=datetime.now())
        db.session.add(clazz)
        db.session.flush()

        #self.lecture_dt = datetime.now()
        class_lecture = ClassLecture(class_id=clazz.id, lecture_id=lecture.id, dt=datetime.now())
        db.session.add(class_lecture)
        db.session.flush()
        db.session.commit()

        self.class_lecture_id = class_lecture.id



    def assert_lecture_first_update(self, lecture_dt):
        q = db.session.query(Lecture, ClassLecture).join(ClassLecture).filter(ClassLecture.id == self.class_lecture_id)
        lecture, class_lecture = q.one()

        self.assertEquals(lecture.name, 'Lecture 100')
        self.assertEquals(lecture.description, 'Description 100')
        self.assertEquals(class_lecture.dt, lecture_dt)  # self.lecture_dt)
        self.assertEquals(lecture.parent_id, self.original_lecture_id)

        # If I dont delete thsese, the next query down below gets stale data for some reason -- why does this happen?
        del lecture
        del class_lecture

        original_lecture = db.session.query(Lecture).filter_by(id=self.original_lecture_id).one()
        self.assertEquals(original_lecture.id, self.original_lecture_id)

    def assert_lecture_second_update(self, lecture_dt):

        ## Update the class lecture for the second time


        print "class_lecture_id is ", self.class_lecture_id
        q = db.session.query(Lecture, ClassLecture).join(ClassLecture).filter(ClassLecture.id == self.class_lecture_id)
        lecture, class_lecture = q.one()
        self.assertEquals(lecture.name, 'Lecture 1000')
        self.assertEquals(lecture.description, 'Description 1000')
        self.assertEquals(class_lecture.dt, lecture_dt)
        self.assertEquals(lecture.parent_id, self.original_lecture_id)

    def test_rest_update_lecture(self):
        '''
        This is when a teacher "updates" a class lecture for the first time
            which actually creates a new Lecture using the old Course Lecture, makes the changes
            and switches the lecture_id in ClassLecture to point to the new Lecture
        '''

        # Update the class lecture for the very first time
        lecture_dt = datetime(year=2017, month=1, day=1, hour=0, minute=0, second=0)
        r = update_class_lecture(class_lecture_id=self.class_lecture_id, name='Lecture 100', description='Description 100', dt=lecture_dt)
        self.assertEquals(r.status_code, 200)
        # Todo: check data response

        self.assert_lecture_first_update(lecture_dt)

        lecture_dt = datetime(year=2018, month=2, day=2, hour=2, minute=2, second=2)
        r = update_class_lecture(class_lecture_id=self.class_lecture_id, name='Lecture 1000', description='Description 1000', dt=lecture_dt)
        self.assertEquals(r.status_code, 200)

        self.assert_lecture_second_update(lecture_dt)
        # Todo: check data response

    def test_function_update_lecture(self):
        app = Flask(__name__)
        lecture_dt = datetime(year=2017, month=1, day=1, hour=0, minute=0, second=0)
        data = {
            'data': [
                {
                    'class_lecture_id': self.class_lecture_id,
                    'name': 'Lecture 100',
                    'description': 'Description 100',
                    'dt': lecture_dt.strftime(date_format)
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # First update
        with app.test_request_context(headers=headers, data=json.dumps(data)):
            r = hardcore_update(Lecture)
            self.assertEquals(r[1], 200)
            # Todo: check data response
            import time
            time.sleep(2)
            self.assert_lecture_first_update(lecture_dt)

        data['data'][0]['name'] = 'Lecture 1000'
        data['data'][0]['description'] = 'Description 1000'
        lecture_dt = datetime(year=2018, month=2, day=2, hour=2, minute=2, second=2)
        data['data'][0]['dt'] = lecture_dt.strftime(date_format)

        #Second update
        with app.test_request_context(headers=headers, data=json.dumps(data)):
            r = hardcore_update(Lecture)
            self.assertEquals(r[1], 200)
            # TODO check data response
            self.assert_lecture_second_update(lecture_dt)


class TestDeleteHomework(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)
        create_interference()

        course = Course(name='Python 101')
        db.session.add(course)

        homework = Homework(name='Homework 2')
        db.session.add(homework)

        homework2 = Homework(name='Homework 2')
        db.session.add(homework2)

        db.session.flush()

        course_homework = CourseHomework(course_id=course.id, homework_id=homework.id)
        course_homework2 = CourseHomework(course_id=course.id, homework_id=homework2.id)

        db.session.add(course_homework)
        db.session.add(course_homework2)

        clazz = Class(course_id=course.id, name='Python 101 2016', start_dt=datetime.now(), end_dt=datetime.now())
        db.session.add(clazz)
        db.session.flush()

        class_homework = ClassHomework(class_id=clazz.id, homework_id=homework.id)
        class_homework2 = ClassHomework(class_id=clazz.id, homework_id=homework2.id)
        db.session.add(class_homework)
        db.session.add(class_homework2)

        db.session.commit()

        self.homework_id = homework.id
        self.homework2_id = homework.id
        self.course_homework_id = course_homework.id
        self.course_homework2_id = course_homework.id
        self.class_homework_id = class_homework.id
        self.class_homework2_id = class_homework2.id

    def test_delete_homework_by_id(self):
        r = delete_homework(self.homework_id)
        self.assertEquals(r.status_code, 200)

        self.assertRaises(NoResultFound, db.session.query(Homework).filter_by(id=self.homework_id).one)




class TestInitializations(unittest.TestCase):
    '''
    When a new Student is added to a Class, all Assignments and Attendance should be initialized for him

    When a new Homework is added to a Class, Assignments should be initialized for all Students

    When a new Lecture is added to a Class, Attendances should be initialized for all Students

    I need to instantiate for when a PUT occurs on a Class Lecture/ClassHomework ...
    '''
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)
        create_interference()


    def _read_attendance_by_class_lecture(self, class_lecture_id):
        api = '/api/attendance/'
        params = {'class_lecture_id': class_lecture_id}
        return hit_api(api, method='GET', params=params)

    def _read_assignment_by_class_homework(self, class_homework_id):
        api = '/api/assignment/'
        params = {'class_homework_id': class_homework_id}
        return hit_api(api, method='GET', params=params)

    def assert_instantiated_attendance(self, attendance, class_lecture_id, class_student_id, class_id, lecture_id,
                                       student_id):
        '''
        This proves that the attendance has been instantiated in either of these two cases:
            Create Class, create Lecture on Class, create Student on Class
            Create Class, create Student on Class, create Lecture on Class
        :param attendance:
        :param class_lecture_id:
        :param class_student_id:
        :param class_id:
        :param lecture_id:
        :param student_id:
        :return:
        '''

        self.assertEquals(attendance['class_lecture_id'], class_lecture_id)
        self.assertEquals(attendance['class_student_id'], class_student_id)
        # attendance defaults to False
        self.assertEquals(attendance['did_attend'], False)
        self.assertEquals(attendance['class']['id'], class_id)
        self.assertEquals(attendance['class']['name'], "Spring 2016")
        self.assertEquals(attendance['lecture']['id'], lecture_id)
        self.assertEquals(attendance['lecture']['name'], 'Lecture 1')
        self.assertEquals(attendance['student']['id'], student_id)
        self.assertEquals(attendance['student']['first_name'], 'Chandler')

    def assert_instantiated_assignment(self, assignment, class_homework_id, class_student_id, class_id, homework_id,
                                       student_id):

        self.assertEquals(assignment['class_homework_id'], class_homework_id)
        self.assertEquals(assignment['class_student_id'], class_student_id)
        self.assertEquals(assignment['class']['id'], class_id)
        self.assertEquals(assignment['class']['name'], "Spring 2016")
        self.assertEquals(assignment['homework']['id'], homework_id)
        self.assertEquals(assignment['homework']['name'], 'Homework 1')
        self.assertEquals(assignment['student']['id'], student_id)
        self.assertEquals(assignment['student']['first_name'], 'Chandler')

    def test_add_student(self):
        '''
        This creates a Course, a Class, a Homework on Class, a Homework on Class, and then a Student on Class
            in that order.
        Creating the student on class should instantiate the Assignments and Attendances.
        '''
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Lecture and Add to Class Synchronously
        r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)
        class_lecture_id = get_first_id_from_response(r, id_key='class_lecture_id')


        ## Create Dependent Homework and Add to Class Synchronously
        r = create_class_homework(class_id=class_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)
        homework_id = get_first_id_from_response(r)
        class_homework_id = get_first_id_from_response(r, id_key='class_homework_id')


        ############
        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        student_id = get_first_id_from_response(r)
        class_student_id = get_first_id_from_response(r, id_key='class_student_id')

        ############
        ## Query for proof

        ## Attendance
        r = self._read_attendance_by_class_lecture(class_lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]

        self.assert_instantiated_attendance(attendance=attendance, class_lecture_id=class_lecture_id,
                                            class_student_id=class_student_id, class_id=class_id, lecture_id=lecture_id,
                                            student_id=student_id)


        ## Assignments
        r = self._read_assignment_by_class_homework(class_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assert_instantiated_assignment(assignment=assignment, class_homework_id=class_homework_id,
                                            class_student_id=class_student_id, class_id=class_id,
                                            homework_id=homework_id, student_id=student_id)




    def test_add_lecture(self):
        '''
        This creates a Course, Class, Student on Class, and Lecture on Class, in that order.
        Creating the Lecture on Class should instantiate the Attendence
        '''
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)


        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        student_id = get_first_id_from_response(r)
        class_student_id = get_first_id_from_response(r, id_key='class_student_id')

        #######
        ## Create Lecture
        r = create_class_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)
        class_lecture_id = get_first_id_from_response(r, id_key='class_lecture_id')

        # Query Attendance for proof
        r = self._read_attendance_by_class_lecture(class_lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]


        self.assert_instantiated_attendance(attendance=attendance, class_lecture_id=class_lecture_id,
                                            class_student_id=class_student_id, class_id=class_id, lecture_id=lecture_id,
                                            student_id=student_id)

    def test_add_homework(self):
        '''
        This creates a Course, Class, Student on Class, and Homework on Class, in that order.
        Creating the Homework on Class should instantiate the Assignment.
        '''
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        student_id = get_first_id_from_response(r)
        class_student_id = get_first_id_from_response(r, id_key='class_student_id')

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_class_homework(class_id=class_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)

        homework_id = get_first_id_from_response(r)
        class_homework_id = get_first_id_from_response(r, id_key='class_homework_id')


        ## Query Assignments for Proof
        ## Assignments
        r = self._read_assignment_by_class_homework(class_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assert_instantiated_assignment(assignment=assignment, class_homework_id=class_homework_id,
                                            class_student_id=class_student_id, class_id=class_id,
                                            homework_id=homework_id, student_id=student_id)








class TestException(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

    def test_class_fk(self):
        '''
        Test exception path for creating a class with a bad foreign key
        '''
        ## Create Course
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=10, name="Spring 2016", start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 400)

        j = r.json()

        self.assertEquals(j['error'], "(sqlite3.IntegrityError) foreign key constraint failed")


class TestParseDataFromQueryArgs(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    def test_happy(self):

        with self.app.test_request_context('?data=foo,bar,baz'):
            foo, bar, baz, hai = parse_data_from_query_args(['foo','bar','baz', 'hai'])

            self.assertEquals(foo, True)
            self.assertEquals(bar, True)
            self.assertEquals(baz, True)
            self.assertEquals(hai, False)

    def test_happy_trailing_comma(self):

        with self.app.test_request_context('?data=foo,bar,baz,'):
            foo, bar, baz, hai = parse_data_from_query_args(['foo','bar','baz', 'hai'])

            self.assertEquals(foo, True)
            self.assertEquals(bar, True)
            self.assertEquals(baz, True)
            self.assertEquals(hai, False)

    def test_happy_no_data(self):
        with self.app.test_request_context():
            foo, bar = parse_data_from_query_args(['foo','bar'])

            self.assertEquals(foo, False)
            self.assertEquals(bar, False)

    def test_differing_server_keys(self):
        with self.app.test_request_context('?data=foo,bar'):
            hai, bai = parse_data_from_query_args(['hai', 'bai'])

            self.assertEquals(hai, False)
            self.assertEquals(bai, False)

class TestParseIdFromQueryArgs(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)


    def test_happy(self):
        with self.app.test_request_context('?course_id=2&class_id=5'):
            course_id, class_id = parse_id_from_query_args(['course_id', 'class_id'])

            self.assertEquals(course_id, 2)
            self.assertEquals(class_id, 5)

    def test_differing_server_keys(self):
        with self.app.test_request_context('?course_id=2&class_id=5'):
            student_id, lecture_id = parse_id_from_query_args(['student_id', 'lecture_id'])

            self.assertEquals(student_id, False)
            self.assertEquals(lecture_id, False)

    def test_bad_int(self):
        with self.app.test_request_context('?foo=bar'):
            self.assertRaises(UserError, parse_id_from_query_args, ['foo'])
            try:
                parse_id_from_query_args(['foo'])
            except UserError as ex:
                self.assertEquals(ex.message, "id must be int, not 'bar'")


class TestExtractData(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.data = json.dumps({
            "data": {
                "foo": "bar"
            }
        })
        self.headers = {
            'Content-Type': 'application/json'
        }

    def test_happy(self):
        with self.app.test_request_context(headers=self.headers, data=self.data):
            data = extract_data()
            self.assertEquals(data, {'foo': 'bar'})

    def test_no_json_header(self):
        with self.app.test_request_context(data=self.data):
            self.assertRaises(UserError, extract_data)

            try:
                extract_data()
            except UserError as ex:
                self.assertEquals(ex.message, "Set Content-Type: application/json")

    def test_no_data_attribute(self):
        data = json.dumps({'foo': 'bar'})
        with self.app.test_request_context(headers=self.headers, data=data):
            self.assertRaises(UserError, extract_data)

            try:
                extract_data()
            except UserError as ex:
                self.assertEquals(ex.message, "Data attribute is required in request")

class TestJsonToModel(unittest.TestCase):
    def setUp(self):
        self.model = Class
        self.obj = {
            'course_id': 1,
            'id': 2,
            'name': 'Test',
            'start_dt': '2016-01-01 00:00:00'
        }
        self.keys = ['course_id', 'id', 'name', 'start_dt']

    def test_happy(self):


        model_inst = json_to_model(model=self.model, obj=self.obj, keys=self.keys)

        self.assertEquals(model_inst.course_id, 1)
        self.assertEquals(model_inst.id, 2)
        self.assertEquals(model_inst.name, 'Test')
        self.assertEquals(model_inst.start_dt, datetime.strptime('2016-01-01 00:00:00', date_format))

    def test_happy_model_inst(self):
        '''
        The model_inst arg on json_to_model should allow a reference to a model be mutated successfully
        '''

        model_inst = Class(course_id=10, id=20, name='Foo', start_dt=datetime.now())

        json_to_model(model=self.model, obj=self.obj, keys=self.keys, model_inst=model_inst)

        self.assertEquals(model_inst.course_id, 1)
        self.assertEquals(model_inst.id, 2)
        self.assertEquals(model_inst.name, 'Test')
        self.assertEquals(model_inst.start_dt, datetime.strptime('2016-01-01 00:00:00', date_format))

    def test_key_not_in_obj(self):
        self.keys.append('foo')

        self.assertRaises(UserError, json_to_model, model=self.model, obj=self.obj, keys=self.keys)

        try:
            json_to_model(model=self.model, obj=self.obj, keys=self.keys)
        except UserError as ex:
            self.assertEquals(ex.message, "Expecting these attributes: {}".format(self.keys))

    def test_bad_date_format(self):
        self.obj['start_dt'] = '2016-01-01'

        self.assertRaises(UserError, json_to_model, model=self.model, obj=self.obj, keys=self.keys)

        try:
            json_to_model(model=self.model, obj=self.obj, keys=self.keys)
        except UserError as ex:
            self.assertEquals(ex.message, "Bad date format: time data '2016-01-01' does not match format '%Y-%m-%d %H:%M:%S'")

    def test_key_not_in_model(self):
        self.obj['foo'] = 'bar'
        self.keys.append('foo')

        self.assertRaises(ServerError, json_to_model, model=self.model, obj=self.obj, keys=self.keys)

        try:
            json_to_model(model=self.model, obj=self.obj, keys=self.keys)
        except ServerError as ex:
            self.assertEquals(ex.message, "type object 'Class' has no attribute 'foo'")



if __name__ == '__main__':
    import nose
    nose.run()


