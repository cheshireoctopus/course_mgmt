__author__ = 'mmoisen'

from course_mgmt import app
from course_mgmt.models import *
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from . import UserError
from . import ServerError



'''
In shell for testing:

from course_mgmt import app, db
from course_mgmt.models import *
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound



'''

def extract_form(form, keys=None):
    '''
    Helper method to extract specified keys out of a POSTed form
    :param form: a dict, should be request.json
    :param keys: list of values expected
    :return: tuple

    Use it like this:
    try:
        foo, bar, baz = extract_form(request.json, ['foo', 'bar', 'baz']
        foo, = extract_form(request.json, ['foo'])
        # ...
    except UserError as ex:
        #...

    Remember that if you only need one variable, place the ',' after it or else you will get this error when adding
    (sqlite3.InterfaceError) Error binding parameter 0 - probably unsupported type.
    '''

    if keys is None:
        raise ServerError("Keys can't be None in extract_form()")

    # If keys is a single argument instead of a list, change it to a list
    if type(keys) not in (list, tuple):
        keys = [keys]

    ret = []
    try:
        for key in keys:
            ret.append(form[key])
    except KeyError as ex:
        raise UserError('Expected key not found in posted form: {}'.format(ex.message))

    # Return a single value instead of a tuple if keys contained only 1 row
    if len(ret) == 1:
        return ret[0]

    return tuple(ret)

def try_except(func):
    '''
    Boiler plate code to reduce exception catching in route calls.
    This wraps all the routes in a try except that catches UserError, ServerError, and Exception
        and fails gracefully by returning a correct json

    For all the routes do this:

    @app.route('/hello/')
    @try_except
    def hello():

        try:
            print 10 / user_submitted_value
        except ZeroDivisionError as ex:
            raise UserError(ex.message)

        try:
            # Do something on the back end
        except SomeBackEndException as ex:
            raise ServerError(ex.message)

    '''
    @wraps(func)
    def _try_except(*args, **kwargs):
        try:
            app.logger.debug("In {}, args={}, kwargs={}".format(func.func_name, args, kwargs))
            return func(*args, **kwargs)

        except BadRequest as ex:
            app.logger.exception(ex)
            return jsonify({'error': 'Invalid JSON request {}'.format(ex.message)}), 400

        except UserError as ex:
            app.logger.exception(ex.message)
            db.session.rollback()
            return jsonify({'error': ex.message}), 400

        except ServerError as ex:
            app.logger.exception(ex.message)
            db.session.rollback()
            return jsonify({'error': ex.message}), 500

        except SQLAlchemyError as ex:
            ''' This is a server error '''
            app.logger.exception(ex.message)
            db.session.rollback()
            return jsonify({'error': ex.message}), 500

        except Exception as ex:
            app.logger.exception(ex.message)
            db.session.rollback()
            return jsonify({'error': ex.message}), 500

    return _try_except


def model_get_all(model):
    '''
    This returns all the data in a given model
    :param model: a Model class
    :returns a list of Model instances
    '''
    app.logger.debug("In model_get_all for {}".format(model.plural))
    try:
        datas = [data.json for data in db.session.query(model).all()]

    except SQLAlchemyError as ex:
        raise ServerError(ex.message)

    return jsonify({'meta': {'len': len(datas)}, 'data': datas})

def model_delete_all(model):
    '''
    Delete all rows for a given model
    :param model: a Model class
    :returns number of deleted rows
    '''
    try:
        num_deleted = db.session.query(model).delete()

    except SQLAlchemyError as ex:
        raise ServerError(ex.message)

    return jsonify({'meta': {'number_deleted': num_deleted}, 'data': None})

def model_get_by_id(model, id):
    '''
    This returns an object from a model given a primary key id
    :param model: a Model class
    :param id: a primary key value
    :returns: a instance of Model
    '''
    app.logger.debug("id is {}".format(id))
    try:
        obj = db.session.query(model).filter_by(id=id).one()
    except NoResultFound as ex:
        raise UserError("No {} with id={}".format(model.__tablename__, id))

    return jsonify({'meta': {}, 'data': obj.json})


def create_dynamic_route(func, model):
    '''
    This function is necessary to get the following for loop to work correctly.
    Defining the function inline the for loop doesn't work for some reason.
    '''
    @try_except
    def _dynamic_route(*args, **kwargs):
        return func(model, *args, **kwargs)

    return _dynamic_route


#_get_by_id = create_dynamic_route(model_get_by_id, Course)

#app.add_url_rule('/api/{}/id/<int:id>/'.format('courses'), '{}_get_by_id'.format('courses'), _get_by_id, methods=['GET'])

'''
This creates "get_all" and "delete_all" views for all the models in all_models
'''
for model in all_models:
    _get_all = create_dynamic_route(model_get_all, model)
    app.add_url_rule('/api/{}/'.format(model.plural), '{}_get_all'.format(model.plural), _get_all, methods=['GET'])

    _get_by_id = create_dynamic_route(model_get_by_id, model)
    app.add_url_rule('/api/{}/<int:id>/'.format(model.plural), '{}_get_by_id'.format(model.plural), _get_by_id, methods=['GET'])

    #_get_by_id = create_dynamic_route(model_get_by_id, model)
    #app.add_url_rule('/api/{}/id/<int:id>/'.format(model.plural), '{}_get_by_id'.format(model.plural), _get_by_id, methods=['GET'])

    #@try_except
    #def _get_by_id(id):
    #    return model_get_by_id(model, id)

    #app.add_url_rule('/api/{}/id/<int:id>/'.format(model.plural), '{}_get_by_id'.format(model.plural), _get_by_id, methods=['GET'])


    _delete_all = create_dynamic_route(model_delete_all, model)
    app.add_url_rule('/api/{}/'.format(model.plural), '{}_delete_all'.format(model.plural), _delete_all, methods=['DELETE'])


def save_obj(obj):
    '''
    Helper method to save a single object to the database
    Note that this will commit, so don't use this if you are saving two objects depending on each other
    :param obj: a instance of a model to be saved
    :returns None
    '''
    try:
        db.session.add(obj)
        db.session.commit()

    except IntegrityError as ex:
        raise UserError(ex.message)

    except SQLAlchemyError as ex:
        raise ServerError(ex.message)


def save_bulk(model, data, keys):
    '''
    Helper method to bulk save a single parent model
    This does not commit so make sure to do so elsewhere.
    :param model: A parent Model (Course, Student, Homework)
    :param data: A list of dicts
    :param keys: the keys for the dicts, fieldnames for this Model

    :return: list of DB objects
    '''
    try:
        # objs = [model(**{key: obj[key] for key in keys}) for obj in data ]
        # Unforunately the above won't work because of date
        # There must be a better way of doing this

        objs = []
        for obj in data:
            kwargs = {}
            for key in keys:
                app.logger.debug(key)
                if isinstance(getattr(model, key).type, DateTime):
                    app.logger.debug("WTF")
                    kwargs[key] = datetime.strptime(obj[key], date_format)
                else:
                    kwargs[key] = obj[key]

            app.logger.debug("kwargs are {}".format(kwargs))
            objs.append(model(**kwargs))

    except KeyError as ex:
        raise UserError("Expecting {}".format(keys))

    db.session.bulk_save_objects(objs, return_defaults=True)

    return objs


'''
@app.route('/api/{}/'.format(Course.plural), methods=['GET'])
@try_except
def course_get_all():
    return model_get_all(Course)
'''


@app.route('/api/drop/', methods=['POST','GET'])
@try_except
def drop_db():
    '''
    REEMOVE THIS METHOD ITS ONLY FOR DEVELOPING
    Drops and recreates the db
    :return:
    '''
    db.drop_all()
    db.create_all()
    return jsonify({}), 200

@app.route('/api/courseaa/', methods=['POST'])
@try_except
def course_create():
    '''
    Creates 1 or more courses.

    Request should be:
        {
            "data": [
                {"name": "Javascript 101"},
                {"name": "Python 101"}
            ]
        }

    :return: JSON containing a list of courses created and their ids
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    courses = [Course(name=course['name']) for course in data]

    app.logger.debug(courses)
    for course in courses:
        app.logger.debug(course.name)

    # Set return_defaults=True if you want the primary keys returned
    try:
        db.session.bulk_save_objects(courses, return_defaults=True)
    except IntegrityError as ex:
        # Because we are doing a bulk save, what if only one of 10 fail with a Unique Constraing violation?
        # This will return the parameters used on the particular row that failed
        raise UserError("{} on {}".format(ex.message, ex.params))

    db.session.commit()

    courses = [course.json for course in courses]

    return jsonify({"meta": {'len':len(courses)}, "data": courses}), 200

#TODO update/put Course

@app.route('/api/course/<int:id>/class/', methods=['GET'])
@try_except
def course_get_classes_by_course_id(id):
    '''
    Find all the Classes for a given Course
    :param id: a Course ID
    :return: a list of classes
    '''

    #TODO How should this be ordered?
    classes = [class_obj.json for class_obj in db.session.query(Class).filter_by(course_id=id)]

    return jsonify({'meta': {'len': len(classes)}, 'data': classes})

@app.route('/api/course/<int:course_id>/homework/', methods=['GET'])
@try_except
def course_get_homework_by_course_id(course_id):
    q = db.session.query(Homework).join(CourseHomework).filter(CourseHomework.course_id == course_id)
    homeworks = [homework.json for homework in q]

    return jsonify({"meta": {"len": len(homeworks)}, "data": homeworks}), 200

@app.route('/api/class/<int:class_id>/homework/', methods=['GET'])
def class_get_homework_by_class_id(class_id):
    q = db.session.query(Homework, CourseHomework).join(CourseHomework).join(Course).join(Class) \
        .filter(Class.id == class_id)

    ret = []
    for homework, course_homework in q:
        ret.append({
            'homework': homework.json,
            'course_homework': course_homework.json
        })

    return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

@app.route('/api/class/<int:class_id>/assignment/', methods=['GET'])
@try_except
def class_get_assignment_by_class_id(class_id):
    '''
    Use this to find the assignments for a class.
    An Assignment is a CourseHomework that is attached with a ClassStudent
    Call the URL with a query parmeter like this:

        /api/class/1/assignment/?course_homework_id=1
    :param class_id:
    :return:
    '''
    args = request.args
    course_homework_id = args.get('course_homework_id', None)
    app.logger.debug("args is {}".format(args))
    app.logger.debug("course_homework_id is {}".format(course_homework_id))

    q = db.session.query(Homework, Assignment, Student) \
        .join(CourseHomework).join(Assignment).join(ClassStudent).join(Student) \
        .filter(ClassStudent.class_id ==class_id)

    if course_homework_id:
        q = q.filter(Assignment.course_homework_id == course_homework_id)

    app.logger.debug("query is {}".format(q.statement))

    ret = []

    for homework, assignment, student in q:
        ret.append(
            {
                'homework': homework.json,
                'assignment': assignment.json,
                'student': student.json,
            }
        )

    return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

@app.route('/api/student/<int:student_id>/assignment/', methods=['GET'])
@try_except
def student_get_assignments_by_student_id(student_id):
    q = db.session.query(Homework, Assignment) \
        .join(CourseHomework).join(Assignment).join(ClassStudent) \
        .filter(ClassStudent.student_id == student_id)

    ret = []

    for homework, assignment in q:
        ret.append(
            {
                'homework': homework.json,
                'assignment': assignment.json
            }
        )

    return jsonify({"meta": {"len": len(ret)}, "data": ret})



@app.route('/api/class/', methods=['POST'])
@try_except
def class_create():
    '''
    Creates one or more classes

    Request should be:
        {
            "data": [
                {"course_id": 1, "start_dt": "2015-01-01 00:00:00", "end_dt": "2015-06-06"},
                {"course_id": 1, "start_dt": "2015-01-01 00:00:00", "end_dt": "2015-06-06"},
            ]
        }

    Note that course_id is just repeated here since we are adding Classes to a Course.
        Perhaps that should go in a "meta" dict?

    :return: a JSON dict containing a list of the created Classes and their IDs
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    date_format = '%Y-%m-%d %H:%M:%S'

    try:
        classes = [Class(course_id=class_obj['course_id'],
                         start_dt=datetime.strptime(class_obj['start_dt'], date_format),
                         end_dt=datetime.strptime(class_obj['end_dt'], date_format))
                   for class_obj in data
        ]
    except KeyError as ex:
        raise UserError(ex.message)

    try:
        db.session.bulk_save_objects(classes, return_defaults=True)
    except IntegrityError as ex:
        raise UserError("{} on {}".format(ex.message, ex.params))

    db.session.commit()

    classes = [class_obj.json for class_obj in classes]

    return jsonify({"meta": {'len': len(classes)}, "data": classes})



'''STUDENT'''

@app.route('/api/student/', methods=['POST'])
@try_except
def student_create():
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    try:
        students = [Student(first_name=student['first_name'],
                            last_name=student['last_name'],
                            github_username=student['github_username'],
                            email=student['email'],
                            photo_url=student['photo_url'])
                    for student in data]
    except KeyError as ex:
        raise UserError("Expecting (first_name, last_name, github_username, email, photo_url)")

    db.session.bulk_save_objects(students, return_defaults=True)

    db.session.commit()

    students = [student.json for student in students]

    return jsonify({"meta": {'len': len(students)}, "data": students}), 200


@app.route('/api/class/<int:class_id>/student/', methods=['POST'])
@try_except
def class_add_student(class_id):
    '''
    Adds a student to a class.
    This also instantiates all Attendance and Assignments.

    There are two ways to hit this API:
        Student has already been created:
            {'student_id': 1}
        Student has not already been created:
            {'first_name': 'Matthew', 'last_name': 'Moisen'}

    :return: ClassStudent
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    try:
        class_students = [ClassStudent(class_id=class_id,
                                       student_id=class_student['student_id'])
                          for class_student in data]
    except KeyError as ex:
        try:
            students = save_bulk(Student, data, ['first_name', 'last_name', 'github_username', 'email', 'photo_url'])

        except UserError as ex:
            raise UserError("Expecting either (class_id, student_id) or (class_id, first_name, last_name, github_username, email, photo_url")

        class_students = [ClassStudent(class_id=class_id,
                                       student_id=student.id)
                          for student in students]

    db.session.bulk_save_objects(class_students, return_defaults=True)

    # Create attendance records for the students
    lecture_ids = [lecture.id for lecture in db.session.query(Lecture).filter_by(class_id=class_id)]
    if lecture_ids:
        attendances = []
        for lecture_id in lecture_ids:
            for class_student in class_students:
                attendances.append(Attendance(lecture_id=lecture_id,
                                              class_student_id=class_student.id))

        db.session.bulk_save_objects(attendances, return_defaults=False)

    # Create assignment records for the students
    q = db.session.query(CourseHomework).join(Course).join(Class).filter(Class.id == class_id)
    course_homework_ids = [course_homework.id for course_homework in q]
    if course_homework_ids:
        assignments = []
        for course_homework_id in course_homework_ids:
            for class_student in class_students:
                assignments.append(Assignment(class_student_id=class_student.id,
                                              course_homework_id=course_homework_id))

        db.session.bulk_save_objects(assignments, return_defaults=False)

    db.session.commit()

    class_students = [class_student.json for class_student in class_students]

    return jsonify({"meta": {'len': len(class_students)}, "data": class_students})


@app.route('/api/homework/', methods=['POST'])
@try_except
def homework_create():
    '''
    Creates 1 or more homeworks.

    Request should be:
        {
            "data": [
                {"name": "hmk1"}
            ]
        }
    '''

    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    homeworks = save_bulk(Homework, data, ['name'])

    db.session.commit()

    homeworks = [homework.json for homework in homeworks]

    return jsonify({"meta": {"len": len(homeworks)}, "data": homeworks}), 200

@app.route('/api/course/<int:course_id>/homework/', methods=['POST'])
@try_except
def course_add_homework(course_id):
    '''
    Adds a homework to a Course.

    TODO: This needs to instantiate the assignments for all students in the class
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)


    # The following permits us to add independent homeworks or dependent homeworks
    try:
        course_homeworks = [CourseHomework(course_id=course_id,
                                          homework_id=homework['homework_id'])
                            for homework in data]
    except KeyError as ex:
        try:
            homeworks = save_bulk(Homework, data, ['name'])
        except UserError as ex:
            raise UserError("expecting either (homework_id) or (name)")

        course_homeworks = [CourseHomework(course_id=course_id,
                                          homework_id=homework.id)
                           for homework in homeworks]

    db.session.bulk_save_objects(course_homeworks, return_defaults=True)

    # Create assignment records
    q = db.session.query(ClassStudent).join(Class).filter(Class.course_id == course_id)
    class_student_ids = [class_student.id for class_student in q]
    if class_student_ids:
        assignments = []
        for class_student_id in class_student_ids:
            for course_homework in course_homeworks:
                assignments.append(Assignment(course_homework_id=course_homework.id,
                                              class_student_id=class_student_id))

        db.session.bulk_save_objects(assignments, return_defaults=False)

    db.session.commit()

    course_homeworks = [course_homework.json for course_homework in course_homeworks]

    return jsonify({"meta": {'len':len(course_homeworks)}, "data": course_homeworks})


@app.route('/api/course/<int:course_id>/homework/', methods=['POST'])
@try_except
def course_read_homework(course_id):
    homeworks = [homework.json for homework in db.session.query(Homework)
                                               .join(CourseHomework)
                                               .filter(CourseHomework.course_id == course_id)]

    return jsonify({"meta": {'len': len(homeworks)}, "dt": homeworks})



@app.route('/api/class/<int:class_id>/lecture/', methods=['POST'])
@try_except
def class_create_lecture(class_id):
    '''
    Adds a lecture to a class

    TODO: this needs to instantiate the Attendance for all students
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    for lecture in data:
        lecture['class_id'] = class_id

    lectures = save_bulk(Lecture, data, ['class_id', 'name', 'description', 'dt'])

    # Initialize Attendance
    q = db.session.query(ClassStudent).join(Class).filter(Class.id == class_id)
    class_student_ids = [class_student.id for class_student in q]
    if class_student_ids:
        attendances = []
        for class_student_id in class_student_ids:
            for lecture in lectures:
                attendances.append(Attendance(lecture_id=lecture.id,
                                              class_student_id=class_student_id))

        db.session.bulk_save_objects(attendances, return_defaults=False)

    db.session.commit()

    lectures = [lecture.json for lecture in lectures]

    return jsonify({"meta": {"len": len(lectures)}, "data": lectures})

@app.route('/api/class/<int:class_id>/lecture/', methods=['GET'])
@try_except
def class_read_lectures(class_id):
    lectures = [lecture.json for lecture in db.session.query(Lecture).filter_by(class_id=class_id)]

    return jsonify({"meta": {"len": len(lectures)}, "data": lectures})


'''
ATTENDANCE
'''

@app.route('/api/class/<int:class_id>/attendance/', methods=['GET'])
@try_except
def class_read_attendance(class_id):
    '''
    Initializes or resets all the attendance for a class
    '''
    q = db.session.query(Lecture, Attendance, Student).join(Attendance).join(ClassStudent).join(Student)\
        .filter(Lecture.class_id == class_id)
    '''
    SELECT lecture.id, lecture.name, lecture.dt, lecture.class_id,
            attendance.id, attendance.lecture_id, attendance.class_student_id, attendance.did_attend,
            student.id, student.first_name, student.last_name
    FROM lecture JOIN attendance ON lecture.id = attendance.lecture_id
         JOIN class_student ON class_student.id = attendance.class_student_id
         JOIN student ON student.id = class_student.student_id
    '''
    ret = []
    for lecture, attendance, student in q:
        ret.append(
            {
                "lecture": lecture.json,
                "attendance": attendance.json,
                "student": student.json
            }

        )

    '''
            {
                'lecture_id': lecture.id,
                'lecture_name': lecture.name,
                'lecture_dt': lecture.dt,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'did_attend': attendance.did_attend
            }
    '''

    return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

@app.route('/api/lecture/<int:lecture_id>/attendance/', methods=['GET'])
@try_except
def lecture_read_attendance(lecture_id):
    q = db.session.query(Attendance, Student).join(ClassStudent).join(Student) \
        .filter(Attendance.lecture_id == lecture_id)
    '''
    SELECT attendance.id, attendance.lecture_id, attendance.class_student_id, attendance.did_attend,
            student.id, student.first_name, student.last_name
    FROM attendance JOIN class_student ON class_student.id = attendance.class_student_id
        JOIN student ON student.id = class_student.student_id
    WHERE 1=1
        AND attendance.lecture_id = :lecture_id_1
    '''

    ret = []
    for attendance, student in q:
        ret.append( {
            'student': student.json,
            'attendance': attendance.json
        })

    return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

@app.route('/api/attendance/', methods=['PUT'])
@try_except
def attendance_update():
    '''
    Use this to mark a Student's attendance

    Request should look like:
        {
            "data": [
                {"id": 1, "did_attend": false},
                {"id": 2, "did_attend": true},
            ]
        }
    '''
    form = request.json
    keys = 'data'
    data = extract_form(form, keys)

    #save_bulk(Attendance, data, ['id', 'did_attend'])
    # change this to bulk_update_mappings
    for attendance in data:
        db.session.query(Attendance).filter_by(id=attendance['id']).update({'did_attend': attendance['did_attend']})

    db.session.commit()

    return jsonify({"meta": {}, "data": {}}), 200


'''ASSIGNMENTS'''
@app.route('/api/assignment/', methods=['PUT'])
def assignment_update():
    '''
    Use this to give a grade to an assignment
    Request should look like:
        {
            "data" [

            ]
        }
    '''
    pass


'''
from flask.views import MethodView
class HomeworkAPI(MethodView):
    decorators = [try_except]

    def get(self, id=None):
        if id is None:
            return model_get_all(Homework)

        return model_get_by_id(Homework, id)


    def add_homework_to_course(self, course_id, homeworks):

        course_homeworks = [CourseHomework(course_id=course_id, homework_id=homework.id)
                            for homework in homeworks]

        db.session.bulk_save_objects(course_homeworks, return_defaults=1)

        db.session.commit()

        course_homeworks = [course_homework.json for course_homework in course_homeworks]

        return jsonify({"meta": {'len': len(course_homeworks), "data": course_homeworks}})


    def post(self, course_id=None):

        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

        homeworks = [Homework(name=homework['name'])
                     for homework in data
                     ]

        db.session.bulk_save_objects(homeworks, return_defaults=True)

        if course_id is not None:
            # Does db session stay open when I route across like this?
            return self.add_homework_to_course(course_id, homeworks)

        db.session.commit()

        homeworks = [homework.json for homework in homeworks]

        return jsonify({"meta": {"len": len(homeworks)}, "data": homeworks})

    def delete(self, id=None):
        number_deleted = 0
        if id is None:
            return model_delete_all(Homework)
        else:
            number_deleted = db.session.query(Homework).filter_by(id=id).delete()
            db.session.commit()

        return jsonify({"meta": {"number_deleted": number_deleted}, "data": None})

homework_view = HomeworkAPI.as_view('homework_api')
app.add_url_rule('/api/homeworks/', defaults={'id': None}, view_func=homework_view, methods=['GET'])
app.add_url_rule('/api/homeworks/', defaults={'course_id': None}, view_func=homework_view, methods=['POST'])
app.add_url_rule('/api/homeworks/<int:id>/', view_func=homework_view, methods=['GET', 'DELETE'])
app.add_url_rule('/api/courses/<int:course_id>/add-homework/', view_func=homework_view, methods=['POST'])
'''