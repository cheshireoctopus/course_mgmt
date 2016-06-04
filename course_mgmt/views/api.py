__author__ = 'mmoisen'
from course_mgmt.models import *
from course_mgmt import app
from . import UserError, ServerError
from flask.ext.classy import FlaskView, route
from flask import jsonify, request, url_for, redirect, g, session

from datetime import datetime
date_format = '%Y-%m-%d %H:%M:%S'
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest
from functools import wraps



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

def bulk_save(model, data, keys):
    '''
    Helper method to bulk save a single parent model
    This does not commit so make sure to do so elsewhere.
    :param model: A parent Model (Course, Student, Homework)
    :param data: A list of dicts
    :param keys: the keys for the dicts, fieldnames for this Model
    :param update: if False, an insert is performed; otherwise an update is performed.
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
                if isinstance(getattr(model, key).type, DateTime):
                    kwargs[key] = datetime.strptime(obj[key], date_format)
                else:
                    kwargs[key] = obj[key]

            objs.append(model(**kwargs))

    except KeyError as ex:
        raise UserError("Expecting {}".format(keys))

    app.logger.debug("objs are {}".format(objs))

    try:
        db.session.bulk_save_objects(objs, return_defaults=True)
    except IntegrityError as ex:
        raise UserError(ex.message)

    return objs


def bulk_update(model, data):
    objs = []
    for obj in data:
        kwargs = {}
        for key in obj:
            app.logger.debug("key is {} is it date {}".format(key, isinstance(getattr(model, key).type, Date)))
            if isinstance(getattr(model, key).type, DateTime):
                kwargs[key] = datetime.strptime(obj[key], date_format)
            else:
                kwargs[key] = obj[key]

            objs.append(kwargs)

    app.logger.debug("objs are {}".format(objs))

    try:
        db.session.bulk_update_mappings(model, objs)
    except IntegrityError as ex:
        return UserError(ex.message)



class Key(object):
    def __init__(self, service_ids):
        self.service_ids = service_ids

    def __eq__(self, other):
        return other in self.service_ids

    def __hash__(self):
        return hash(1)

a = Key(['a','b','c'])
b = Key(['d','e','f'])

map = {a: 'a', b: 'b'}


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



class BaseView(FlaskView):
    trailing_slash = True
    model = None
    post_keys = []

    def index(self):
        return self.get(None)

    @try_except
    def get(self, id=None):
        if self.model is None:
            raise NotImplementedError("Define model")

        if id is not None:
            try:
                obj = db.session.query(self.model).filter_by(id=id).one().json
            except NoResultFound as x:
                raise UserError("No {} with id={}".format(self.model.__tablename__, id))

            return jsonify({"meta": {}, "data": obj})

        objs = [obj.json for obj in db.session.query(self.model).all()]

        return jsonify({"meta": {"len": len(objs)}, "data": objs}), 200

    @try_except
    def post(self):
        if self.model is None or not self.post_keys:
            raise NotImplementedError("Define model and post_keys")

        data = request.json['data']

        objs = bulk_save(self.model, data, self.post_keys)

        objs = [obj.json for obj in objs]

        db.session.commit()

        return jsonify({"meta": {"len": len(objs)}, "data": objs}), 200

    @try_except
    def delete(self):
        if self.model is None:
            raise NotImplementedError("Define model")

        delete_all = False

        form = request.json

        # TODO clean this up
        if 'meta' in form:
            if 'delete_all' in form['meta']:
                delete_all = form['meta']['delete_all']

        if delete_all:
            num_deleted = db.session.query(self.model).delete()
        else:
            data = request.json['data']
            ids = [obj['id'] for obj in data]
            num_deleted = 5
            num_deleted = db.session.query(self.model).filter(self.model.id.in_((id for id in ids))).delete(synchronize_session='fetch')

        db.session.commit()

        return jsonify({'meta': {'num_deleted': num_deleted}, 'data': {}}), 200

    @try_except
    def put(self):
        if self.model is None:
            raise NotImplementedError("Define model")

        # TODO need to handle date conversion dynamically
        # Should probably just read sqlalchemy documentation for once and learn to dynamically inspect columns easily

        data = request.json['data']
        if not isinstance(data, list):
            raise UserError({"data attribute should be dict/json"})

        bulk_update(self.model, data)

        db.session.commit()

        return jsonify({'meta': {}, 'data': {}}), 200




class CourseView(BaseView):
    model = Course
    post_keys = ['name']

    @route('/<int:course_id>/class/', methods=['GET'])
    @try_except
    def get_classes(self, course_id):
        classes = [clazz.json for clazz in db.session.query(Class).filter_by(id=course_id)]

        return jsonify({"meta": {"len": len(classes)}, "data": classes}), 200

    @route('/<int:course_id>/homework/', methods=['GET'])
    @try_except
    def course_read_homework(self, course_id):
        homeworks = [homework.json for homework in db.session.query(Homework)
                                                   .join(CourseHomework)
                                                   .filter(CourseHomework.course_id == course_id)]

        return jsonify({"meta": {'len': len(homeworks)}, "dt": homeworks})

    @route('/<int:course_id>/homework/', methods=['POST'])
    @try_except
    def course_add_homework(self, course_id):
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
                homeworks = bulk_save(Homework, data, ['name'])
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


class ClassView(BaseView):
    model = Class
    post_keys = ['start_dt', 'end_dt', 'course_id']

    @route('/<int:class_id>/homework/', methods=['GET'])
    @try_except
    def get_homework(self, class_id):
        q = db.session.query(Homework, CourseHomework).join(CourseHomework).join(Course).join(Class) \
            .filter(Class.id == class_id)

        ret = []
        for homework, course_homework in q:
            ret.append({
                'homework': homework.json,
                'course_homework': course_homework.json
            })

        return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

    @route('/<int:class_id>/lecture/', methods=['GET'])
    @try_except
    def class_read_lectures(self, class_id):
        lectures = [lecture.json for lecture in db.session.query(Lecture).filter_by(class_id=class_id)]

        return jsonify({"meta": {"len": len(lectures)}, "data": lectures})

    @route('/<int:class_id>/assignment/', methods=['GET'])
    @try_except
    def get_assignment(self, class_id):
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

    @route('/<int:class_id>/attendance/', methods=['GET'])
    @try_except
    def class_read_attendance(self, class_id):
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

    @route('/<int:class_id>/lecture/', methods=['POST'])
    @try_except
    def class_create_lecture(self, class_id):
        '''
        Adds a lecture to a class

        TODO: this needs to instantiate the Attendance for all students
        '''
        app.logger.debug("HAI IN CLASS/ID/LECTURE/")
        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

        # This will modify request.json when it arrives in lecture.post, hopefully
        for lecture in data:
            lecture['class_id'] = class_id
        app.logger.debug("ROUTING TO LECTUREVIEW:POST")

        # Why do we use code=307? It directs to the GET if we don't.
        # Why? Not a clue, read this: http://stackoverflow.com/a/15480983/1391717

        g.data = data

        session['data'] = data

        return redirect(url_for('LectureView:post'), code=307)

        lectures = bulk_save(Lecture, data, ['class_id', 'name', 'description', 'dt'])

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

    @route('/<int:class_id>/student/', methods=['POST'])
    @try_except
    def class_add_student(self, class_id):
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
                students = bulk_save(Student, data, ['first_name', 'last_name', 'github_username', 'email', 'photo_url'])

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


class StudentView(BaseView):
    model = Student
    post_keys = ['first_name', 'last_name', 'github_username', 'email', 'photo_url']

    @route('/<int:student_id>/assignment/', methods=['GET'])
    @try_except
    def get_assignment1(self, student_id):
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

    @route('/wtfyo/')
    def wtf(self):
        return 'wtf d'


class LectureView(BaseView):
    model = Lecture
    post_keys = ['name', 'description', 'dt', 'class_id']

    @try_except
    def post(self):
        app.logger.debug("IN SIDE LECTURE VIEW POST")
        app.logger.debug("request.json is {}".format(request.json))
        app.logger.debug("request.form is {}".format(request.json))

        #app.logger.debug(url_for('StudentView:wtf', class_id=1))  # Class.create_class_lecture(class_id)
        #return redirect(url_for('StudentView:wtf', class_id=1))

        #app.logger.debug(url_for('ClassView:class_create_lecture', class_id=1))  # Class.create_class_lecture(class_id)
        #return redirect(url_for('ClassView:class_create_lecture', class_id=1))

        if 'data' in session:
            # If request is from /class/<class_id>/lecture/ it redirects here
            # pull out data from session which is modified with the lecture_id
            data = session.pop('data')
        else:
            form = request.json
            keys = 'data'
            data = extract_form(form, keys)

        #return redirect(url_for('LectureView:post'))

        lectures = bulk_save(Lecture, data, self.post_keys)

        class_ids = ((lecture.class_id for lecture in lectures))

        # Initialize Attendance
        q = db.session.query(ClassStudent).join(Class).filter(Class.id.in_(class_ids))
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

    @route('/<int:lecture_id>/attendance/', methods=['GET'])
    @try_except
    def lecture_read_attendance(self, lecture_id):
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





class HomeworkView(BaseView):
    model = Homework
    post_keys = ['name']

'''
class AttendanceView(BaseView):
    model = Attendance
    post_keys = ['lecture_id', 'class_student_id', 'did_attend']

class AssignmentView(BaseView):
    model = Assignment
    post_keys = ['class_student_id', 'course_homework_id', 'is_completed']
'''

views = [CourseView, ClassView, StudentView, LectureView, HomeworkView]
for view in views:
    view.register(app, route_prefix='/api/', trailing_slash=True)
