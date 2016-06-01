__author__ = 'mmoisen'


import unittest
import requests

URL = 'http://localhost:5000'

def get_first_id_from_response(r):
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
    return r.json()['data'][0]['id']

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
    return hit_api(api)

def create_course(name):
    '''
    Utility function to create a single course
    '''
    api = '/api/course/'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data)

def create_lecture(class_id, name, description, dt):
    # Utility function to create a single lecture
    api = '/api/class/{}/lecture/'.format(class_id)
    data = {
        'data': [
            {
                'name': name,
                'description': description,
                'dt': dt
            }
        ]
    }

    return hit_api(api, data)

def create_class(course_id, start_dt, end_dt):
    '''
    Utility function to create a single class
    '''
    api = '/api/class/'
    data = {
        'data': [
            {
                'course_id': course_id,
                'start_dt': start_dt,
                'end_dt': end_dt
            }
        ]
    }

    return hit_api(api, data)

def create_homework_independent(name):
    # Creates an indepenent homework
    api = '/api/homework/'
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data)

def add_homework_independent_to_course(course_id, homework_id):
    api = '/api/course/{}/homework/'.format(course_id)
    data = {
        'data': [
            {
                'homework_id': homework_id
            }
        ]
    }

    return hit_api(api, data)

def create_homework_dependent(course_id, name):
    api = '/api/course/{}/homework/'.format(course_id)
    data = {
        'data': [
            {
                'name': name
            }
        ]
    }

    return hit_api(api, data)

def create_student_independent(first_name, last_name, github_username, email, photo_url):
    api = '/api/student/'
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

    return hit_api(api, data)

def add_student_independent_to_class(class_id, student_id):
    api = '/api/class/{}/student/'.format(class_id)
    data = {
        'data': [
            {
                'student_id': student_id
            }
        ]
    }

    return hit_api(api, data)

def create_student_dependent(class_id, first_name, last_name, github_username, email, photo_url):
    api = '/api/class/{}/student/'.format(class_id)
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

    return hit_api(api, data)

class TestAll(unittest.TestCase):
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

    def test_all_create(self):
        '''
        This system test hits all of the create APIs happy path
        :return:
        '''
        ## Create Course
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Lecture
        r = create_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        ## Create Independent Homework and add to Course
        # Create Independent Homework
        r = create_homework_independent('Homework 1')
        self.assertEquals(r.status_code, 200)

        homework_independent_id = get_first_id_from_response(r)

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

        # Add Independent Student to Class
        r = add_student_independent_to_class(class_id, student_independent_id)
        self.assertEquals(r.status_code, 200)

        class_student_id_1 = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id_2 = get_first_id_from_response(r)


class TestInitializations(unittest.TestCase):
    '''
    When a new Student is added to a Class, all Assignments and Attendance should be initialized for him

    When a new CourseHomework is added, Assignments should be initialized for all Students

    When a new Lecture is added, Attendances should be initialized for all Students
    '''
    def setUp(self):
        # Drop and recreate the database
        self.assertEquals(200, drop_and_create_db().status_code)

        '''
        Create a completely different course/class/lecture/homework/student to see if it interferes
        '''

        # Course
        r = create_course(name='Interference Course')
        self.assertEquals(r.status_code, 200)
        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)
        class_id = get_first_id_from_response(r)

        ## Create Lecture
        r = create_lecture(class_id=class_id, name='Interference Lecture', description='The first interference', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Interference Homework 2')
        self.assertEquals(r.status_code, 200)

        ############
        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=1, first_name='Inter', last_name='Ference', github_username='interference',
                                     email='inter@ference.com', photo_url='http://interference.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

    def _read_attendance_by_lecture(self, lecture_id):
        api = '/api/lecture/{}/attendance/'.format(lecture_id)
        return hit_api(api, method='GET')

    def _read_assignment(self, class_id, course_homework_id):
        api = '/api/class/{}/assignment'.format(class_id)
        params = {'course_homework_id': course_homework_id}
        return hit_api(api, method='GET', params=params)

    def test_add_student(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Lecture
        r = create_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)
        course_homework_id = get_first_id_from_response(r)


        ############
        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        ############
        ## Query for proof

        ## Attendance
        r = self._read_attendance_by_lecture(lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]

        self.assertEquals(attendance['attendance']['lecture_id'], lecture_id)
        # attendance defaults to False
        self.assertEquals(attendance['attendance']['did_attend'], False)
        #self.assertEquals(attendance['student']['id'], student_id)

        ## Assignments
        r = self._read_assignment(class_id, course_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assertEquals(assignment['assignment']['course_homework_id'], course_homework_id)
        self.assertEquals(assignment['assignment']['class_student_id'], class_student_id)
        self.assertEquals(assignment['homework']['name'], 'Homework 1')



    def test_add_lecture(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)


        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        #######
        ## Create Lecture
        r = create_lecture(class_id=class_id, name='Lecture 1', description='The first lecturel', dt='2016-01-01 00:00:00')
        self.assertEquals(r.status_code, 200)

        lecture_id = get_first_id_from_response(r)

        # Query Attendance for proof
        r = self._read_attendance_by_lecture(lecture_id)
        self.assertEquals(r.status_code, 200)

        attendances = r.json()['data']
        self.assertEquals(1, len(attendances))

        attendance = attendances[0]

        self.assertEquals(attendance['attendance']['lecture_id'], lecture_id)
        # attendance defaults to False
        self.assertEquals(attendance['attendance']['did_attend'], False)
        self.assertEquals(attendance['attendance']['class_student_id'], class_student_id)

    def test_add_homework(self):
        r = create_course(name='Matthew''s Course')
        self.assertEquals(r.status_code, 200)

        course_id = get_first_id_from_response(r)

        ## Create Class
        r = create_class(course_id=course_id, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 200)

        class_id = get_first_id_from_response(r)

        ## Create Dependent Student and Add to Class
        r = create_student_dependent(class_id=class_id, first_name='Chandler', last_name='Moisen', github_username='cheshire',
                                     email='hello@chandlermoisen.com', photo_url='http://chandlermoinse.com/pic.jpg')
        self.assertEquals(r.status_code, 200)

        class_student_id = get_first_id_from_response(r)

        ## Create Dependent Homework and Add to Course Synchronously
        r = create_homework_dependent(course_id=course_id, name='Homework 1')
        self.assertEquals(r.status_code, 200)
        course_homework_id = get_first_id_from_response(r)


        ## Query Assignments for Proof
        ## Assignments
        r = self._read_assignment(class_id, course_homework_id)
        self.assertEquals(r.status_code, 200)

        assignments = r.json()['data']

        self.assertEquals(1, len(assignments))

        assignment = assignments[0]

        self.assertEquals(assignment['assignment']['course_homework_id'], course_homework_id)
        self.assertEquals(assignment['assignment']['class_student_id'], class_student_id)
        self.assertEquals(assignment['homework']['name'], 'Homework 1')
        self.assertEquals(1, 1)








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
        r = create_class(course_id=10, start_dt='2016-01-01 00:00:00', end_dt='2016-05-30 00:00:00')
        self.assertEquals(r.status_code, 400)

        j = r.json()


if __name__ == '__main__':
    import nose
    nose.run()
