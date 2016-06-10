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
from sqlalchemy.orm.session import make_transient
from collections import defaultdict

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


def parse_data_from_query_args(keys):
    '''
    Utility function to extract query args and return boolean values
    Use like this:

        get_homework, get_lecture, get_class = parse_data_from_query_args(['homework','lecture','class'])

        Request should be:
        /api/course/1?data=homework,lecture,class

    :param keys: list of values to parse the data query param with
    :return: a tuple of booleans in the same order as :keys
    '''
    data = request.args.get('data', None)
    ret = {key: False for key in keys}
    if data:
        args = data.lower().split(',')
        for arg in args:
            if arg in keys:
                ret[arg] = True

    return tuple(ret[key] for key in keys)

def parse_id_from_query_args(keys):
    ret = {key: False for key in keys}

    for k, v in request.args.iteritems():
        if k in keys:
            try:
                val = int(v)
            except ValueError:
                raise UserError("id must be int, not {}".format(v))
            ret[k] = val

    return tuple(ret[key] for key in keys)


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


def json_to_model(model, obj, keys, model_inst=None):
    kwargs = {}
    for key in keys:
        if isinstance(getattr(model, key).type, DateTime):
            kwargs[key] = datetime.strptime(obj[key], date_format)
        else:
            kwargs[key] = obj[key]
    if not model_inst:
        model_inst = model(**kwargs)
    else:
        for key in keys:
            setattr(model_inst, key, kwargs[key])

    #m.obj = obj
    return model_inst

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
            m = model(**kwargs)
            m.obj = obj
            objs.append(m)

    except KeyError as ex:
        raise UserError("Expecting {}, got {}".format(keys, ex.message))

    app.logger.debug("objs are {}".format(objs))

    try:
        db.session.bulk_save_objects(objs, return_defaults=True)
    except IntegrityError as ex:
        app.logger.exception("data was {}".format(data))
        app.logger.exception("objs were {}".format(objs))
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




def add_many_to_many(data, strong_id_key, strong_id_value, many_model, weak_model, weak_id_key, weak_keys):
    try:
        many_many = [many_model(**{strong_id_key: strong_id_value, weak_id_key: obj[weak_id_key]}) for obj in data]
    except KeyError as ex:
        try:
            weaks = bulk_save(weak_model, data, weak_keys)
        except UserError as ex:
            raise UserError("Expecting either {} or {}".format(weak_id_key, weak_keys))

        many_many = [many_model(**{strong_id_key: strong_id_value, weak_id_key: weak.id}) for weak in weaks]

    db.session.bulk_save_objects(many_many, return_defaults=True)

    return many_many

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


def extract_data():
    if not request.json:
        raise UserError("Set Content-Type: application/json")
    try:
        data = request.json['data']
    except KeyError as ex:
        raise UserError("Data attribute is required in request")

    return data

class BaseView(FlaskView):
    trailing_slash = True
    model = None
    post_keys = []

    def index(self):
        return self.get(None)

    @try_except
    @route('/<int:id>/', methods=['GET'])
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

        data = extract_data()

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
            num_deleted = db.session.query(self.model).filter(self.model.id.in_((id for id in ids))).delete(synchronize_session='fetch')

        db.session.commit()

        return jsonify({'meta': {'num_deleted': num_deleted}, 'data': {}}), 200

    @try_except
    def put(self):
        if self.model is None:
            raise NotImplementedError("Define model")

        # TODO need to handle date conversion dynamically
        # Should probably just read sqlalchemy documentation for once and learn to dynamically inspect columns easily

        data = extract_data()
        if not isinstance(data, list):
            raise UserError({"data attribute should be array"})

        bulk_update(self.model, data)

        db.session.commit()

        return jsonify({'meta': {}, 'data': {}}), 200





class CourseView(BaseView):
    model = Course
    post_keys = ['name']

    @try_except
    @route('/<int:id>/', methods=['GET'])
    def get(self, id=None):
        app.logger.debug(request.args)

        if id is None:
            courses = [course.json for course in db.session.query(self.model).all()]
            return jsonify({"meta": {"len": len(courses)}, "data": courses}), 200

        get_homework, get_lecture, get_class = parse_data_from_query_args(['homework', 'lecture', 'class'])
        app.logger.debug("{} {} {}".format(get_homework, get_lecture, get_class))
        try:
            course = db.session.query(Course).filter_by(id=id).one()
        except NoResultFound:
            raise UserError("No courses with id={}".format(id))

        ret = course.json

        if get_class:
            ret['classes'] = []
            q = db.session.query(Class).filter(Class.course_id == id)
            for clazz in q:
                ret['classes'].append(clazz.json)
                print (course.json, clazz.json,)

        if get_homework:
            ret['homeworks'] = []
            q = db.session.query(Homework, CourseHomework).join(CourseHomework).filter(CourseHomework.course_id == id)
            for homework, course_homework in q:
                obj = homework.json

                obj['course_homework_id'] = course_homework.id
                ret['homeworks'].append(obj)
                print (homework.json, course_homework.json)

        if get_lecture:
            ret['lectures'] = []
            q = db.session.query(Lecture, CourseLecture).join(CourseLecture).filter(CourseLecture.course_id == id)
            for lecture, course_lecture in q:
                obj = lecture.json

                obj['course_lecture_id'] = course_lecture.id
                ret['lectures'].append(obj)
                print (lecture.json, course_lecture.json)


        return jsonify({"meta": {}, "data": ret})

    @route('/<int:course_id>/class/', methods=['GET'])
    @try_except
    def get_classes(self, course_id):
        classes = [clazz.json for clazz in db.session.query(Class).filter_by(id=course_id)]

        return jsonify({"meta": {"len": len(classes)}, "data": classes}), 200

    @route('/<int:course_id>/homework/', methods=['GET'])
    @try_except
    def course_read_homework(self, course_id):
        '''
        Should this return the associated homework IDs?
        :param course_id:
        :return:
        '''
        homeworks = [homework.json for homework in db.session.query(Homework)
                                                   .join(CourseHomework)
                                                   .filter(CourseHomework.course_id == course_id)]

        return jsonify({"meta": {'len': len(homeworks)}, "data": homeworks})

    @route('/<int:course_id>/lecture/', methods=['GET'])
    @try_except
    def course_read_lecture(self, course_id):
        lectures = [lecture.json for lecture in db.session.query(Lecture)
                                                .join(CourseLecture)
                                                .filter(CourseLecture.course_id == course_id)]

        return jsonify({"meta": {"len": len(lectures)}, "data": lectures})

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
        '''
        # Move this to class homework?
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
        '''

        course_homeworks = [course_homework.json for course_homework in course_homeworks]

        db.session.commit()

        return jsonify({"meta": {'len':len(course_homeworks)}, "data": course_homeworks})

    @route('/<int:course_id>/lecture/', methods=['POST'])
    def course_add_lecture(self, course_id):
        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

        course_lectures = add_many_to_many(data=data, strong_id_key='course_id', strong_id_value=course_id,
                                           many_model=CourseLecture, weak_model=Lecture, weak_id_key='lecture_id',
                                           weak_keys=['name', 'description', 'dt'])
        '''
        try:
            course_lectures = [CourseLecture(course_id=course_id,
                                             lecture_id=lecture['lecture_id'])
                                for lecture in data]

        except KeyError as ex:
            try:
                lectures = bulk_save(Lecture, data, ['name'])
            except UserError as ex:
                app.logger.debug(ex.message)
                raise UserError("expecting either (lecture_id) or (name)")

            course_lectures = [CourseLecture(course_id=course_id,
                                             lecture_id=lecture.id)
                                for lecture in lectures]

        db.session.bulk_save_objects(course_lectures, return_defaults=True)
        '''
        course_lectures = [course_lecture.json for course_lecture in course_lectures]

        db.session.commit()

        return jsonify({"meta": {"len": len(course_lectures)}, "data": course_lectures})

    @route('/<int:course_id>/class/', methods=['POST'])
    def course_add_class(self, course_id):
        '''
        Add course_id to data and route to ClassView.post
        :param course_id:
        :return:
        '''
        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

        for clazz in data:
            clazz['course_id'] = course_id

        session['data'] = data

        return redirect(url_for('ClassView:post'), code=307)






class ClassView(BaseView):
    model = Class
    post_keys = ['name', 'start_dt', 'end_dt', 'course_id']

    @try_except
    def index(self):
        course_id, = parse_id_from_query_args(['course_id'])

        q = db.session.query(Class)
        if course_id:
            q = q.filter_by(course_id=course_id)

        classes = [clazz.json for clazz in q]

        return jsonify({"meta": {"len": len(classes)}, "data": classes}), 200

    @try_except
    @route('/<int:id>/', methods=['GET'])
    def get(self, id=None):

        get_student, get_homework, get_lecture, get_course = parse_data_from_query_args(['student', 'homework', 'lecture', 'course'])

        try:
            clazz = db.session.query(Class).filter_by(id=id).one()
        except NoResultFound:
            raise UserError("No classes with id={}".format(id))

        ret = clazz.json

        if get_student:
            ret['students'] = []
            q = db.session.query(Student, ClassStudent).join(ClassStudent).filter(ClassStudent.class_id == id)
            for student, class_student in q:
                obj = student.json
                obj['class_student_id'] = class_student.id
                ret['students'].append(obj)

        if get_homework:
            ret['homeworks'] = []
            q = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.class_id == id)
            for homework, class_homework in q:
                obj = homework.json
                obj['class_homework_id'] = class_homework.id
                ret['homeworks'].append(obj)

        if get_lecture:
            ret['lectures'] = []
            q = db.session.query(Lecture, ClassLecture).join(ClassLecture).filter(ClassLecture.class_id == id)
            for lecture, class_lecture in q:
                obj = lecture.json
                cl = class_lecture.json  # I need to do this to pull date out in proper format for some reason
                obj['class_lecture_id'] = class_lecture.id
                obj['dt'] = cl['dt']
                ret['lectures'].append(obj)

        if get_course:
            course = db.session.query(Course).filter_by(id=clazz.course_id).one()
            ret['course'] = course.json

        return jsonify({"meta": {}, "data": ret})


    @try_except
    def post(self):
        '''
        When a new class is created
            instantiate the ClassHomework from CourseHomework
            instantiate the ClassLecture from CourseLecture
        :return:
        '''

        if 'data' in session:
            app.logger.debug("data is in session {}".format(session['data']))
            data = session.pop('data')
        else:
            data = extract_data()

        if not isinstance(data, list):
            raise UserError({"data attribute should be dict/json"})

        ## Create Class
        classes = bulk_save(self.model, data, self.post_keys)


        course_ids = [clazz.course_id for clazz in classes]
        class_homeworks = []
        class_lectures = []

        course_homeworks = db.session.query(CourseHomework).filter(CourseHomework.course_id.in_(course_ids)).all()
        course_lectures = db.session.query(CourseLecture).filter(CourseLecture.course_id.in_(course_ids)).all()

        # Try to minimize harm from N^2 loop
        course_homeworks_map, course_lectures_map = defaultdict(list), defaultdict(list)
        for course_homework in course_homeworks:
            course_homeworks_map[course_homework.course_id].append(course_homework)
        for course_lecture in course_lectures:
            course_lectures_map[course_lecture.course_id].append(course_lecture)

        for clazz in classes:
            for course_homework in course_homeworks_map[clazz.course_id]:
                class_homeworks.append(ClassHomework(class_id=clazz.id, homework_id=course_homework.homework_id))

            for course_lecture in course_lectures_map[clazz.course_id]:
                class_lectures.append(ClassLecture(class_id=clazz.id, lecture_id=course_lecture.lecture_id))


        db.session.bulk_save_objects(class_homeworks, return_defaults=False)
        db.session.bulk_save_objects(class_lectures, return_defaults=False)


        classes = [clazz.json for clazz in classes]

        db.session.commit()

        return jsonify({"meta": {"len": len(classes)}, "data": classes})




    @route('/<int:class_id>/homework/', methods=['GET'])
    @try_except
    def class_read_homework(self, class_id):
        q = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.class_id == class_id)

        ret = []
        for homework, class_homework in q:
            ret.append({
                'homework': homework.json,
                'class_homework': class_homework.json
            })

        return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200

    @route('/<int:class_id>/lecture/', methods=['GET'])
    @try_except
    def class_read_lecture(self, class_id):
        q = db.session.query(Lecture, ClassLecture).join(ClassLecture).filter(ClassLecture.class_id == class_id)

        ret = []
        for lecture, class_lecture in q:
            ret.append({
                'lecture': lecture.json,
                'class_lecture': class_lecture.json
            })


        return jsonify({"meta": {"len": len(ret)}, "data": ret})

    @route('/<int:class_id>/assignment/', methods=['GET'])
    @try_except
    def get_assignment(self, class_id):
        '''
        Use this to find the assignments for a class.
        An Assignment is a ClassHomework that is attached with a ClassStudent
        Call the URL with a query parmeter like this:

            /api/class/1/assignment/?class_homework_id=1
        :param class_id:
        :return:
        '''
        args = request.args
        class_homework_id = args.get('class_homework_id', None)
        app.logger.debug("args is {}".format(args))
        app.logger.debug("course_homework_id is {}".format(class_homework_id))

        q = db.session.query(Homework, Assignment, Student) \
            .join(ClassHomework).join(Assignment).join(ClassStudent).join(Student) \
            .filter(ClassStudent.class_id == class_id)

        if class_homework_id:
            q = q.filter(Assignment.class_homework_id == class_homework_id)

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
        Use this to find the Attendance for a Class.
        An Attendance is a ClassLecture that is attached with a ClassStudent
        Call the URL with a query parmeter like this:

            /api/class/1/assignment/?class_lecture_id=1
        '''
        args = request.args
        class_lecture_id = args.get('class_lecture_id', None)

        q = db.session.query(Lecture, Attendance, Student).join(ClassLecture).join(Attendance).join(ClassStudent).join(Student)\
            .filter(ClassStudent.class_id == class_id)

        if class_lecture_id:
            q = q.filter(Attendance.class_lecture_id == class_lecture_id)

        ret = []
        for lecture, attendance, student in q:
            ret.append(
                {
                    "lecture": lecture.json,
                    "attendance": attendance.json,
                    "student": student.json
                }

            )

        return jsonify({"meta": {"len": len(ret)}, "data": ret}), 200




    @route('/<int:class_id>/lecture/', methods=['POST'])
    @try_except
    def class_create_lecture(self, class_id):
        '''
        Adds an Independent Lecture to a Class

        This needs to instantiate the Attendance for all students

        What should I be returning out of this?
            Right now I'm returning ClassLecture
            Before I was returning Lecture
            Should I return (ClassLecture, Lecture) instead?
        '''

        data = extract_data()

        try:
            class_lectures = [ClassLecture(class_id=class_id,
                                           lecture_id=lecture['lecture_id'])
                                for lecture in data]

        except KeyError as ex:
            try:
                lectures = bulk_save(Lecture, data, ['name'])
            except UserError as ex:
                raise UserError("Expecting either (lecture_id) or (name)")

            class_lectures = [ClassLecture(class_id=class_id,
                                           lecture_id=lecture['lecture_id'])
                                for lecture in lectures]

        db.session.bulk_save_objects(class_lectures, return_defaults=True)

        # Initialize Attendance
        q = db.session.query(ClassStudent).filter_by(class_id=class_id)
        class_student_ids = [class_student.id for class_student in q]
        if class_student_ids:
            attendances = []
            for class_student_id in class_student_ids:
                for class_lecture in class_lectures:
                    attendances.append(Attendance(class_lecture_id=class_lecture.id,
                                                  class_student_id=class_student_id))

            db.sesion.bulk_save_objects(attendances, return_defaults=False)

        class_lectures = [class_lecture.json for class_lecture in class_lectures]

        db.session.commit()

        return jsonify({"meta": {"len": len(class_lectures)}, "data": class_lectures})

    @route('/<int:class_id>/homework/', methods=['POST'])
    def class_create_homework(self, class_id):
        pass

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
        data = extract_data()

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

    @try_except
    def index(self):
        class_id, = parse_id_from_query_args(['class_id'])

        if not class_id:
            q = db.session.query(Student)
            students = [student.json for student in q]

        else:
            students = []
            q = db.session.query(Student, ClassStudent).join(ClassStudent).filter(ClassStudent.class_id==class_id)
            for student, class_student in q:
                obj = student.json
                obj['class_student_id'] = class_student.id
                students.append(obj)

        return jsonify({"meta": {}, "data": students})

    @try_except
    @route('/<int:id>/', methods=['GET'])
    def get(self, id=None):
        # TODO should I add assignment and attendance here?
        get_class, get_assignment, get_attendance = parse_data_from_query_args(['class', 'assignment', 'attendance'])

        try:
            student = db.session.query(Student).filter_by(id=id).one()
        except NoResultFound:
            raise UserError("No students with id={}".format(id))

        ret = student.json

        if get_class:
            ret['classes'] = []
            q = db.session.query(Class, ClassStudent).join(ClassStudent).filter(ClassStudent.student_id == student.id)
            for clazz, class_student in q:
                obj = clazz.json
                obj['class_student_id'] = class_student.id
                ret['classes'].append(obj)

        if get_assignment:
            # TODO confirm with Chandler if the return values are fine here
            ret['assignments'] = []
            q = db.session.query(Homework, Assignment, ClassStudent).join(ClassHomework).join(Assignment).join(ClassStudent).filter(ClassStudent.student_id == id)
            for homework, assignment, class_student in q:
                obj = assignment.json
                obj['homework'] = homework.json
                obj['class_student_id'] = class_student.id
                ret['assignments'].append(obj)

        if get_attendance:
            # TODO confirm with Chandler if the return values are fine here
            ret['attendances'] = []
            q = db.session.query(Lecture, Attendance, ClassStudent).join(ClassLecture).join(Attendance).join(ClassStudent).filter(ClassStudent.student_id == id)
            for lecture, attendance, class_student in q:
                obj = attendance.json
                obj['lecture'] = lecture.json
                obj['class_student_id'] = class_student.id
                ret['attendances'].append(obj)

        return jsonify({"meta": {}, "data": ret}), 200

    @try_except
    def post(self):
        data = extract_data()

        # This ensures the order of the response is identical to the request
        ordered_students = []

        # This contains the newly created Students (where "id" is not present)
        students = []

        # Check each obj in data and determine if it is New and/or needs to be associated to a Class
        for obj in data:
            student = Student()

            if 'class_id' in obj:
                student.class_id = obj['class_id']

            if not 'id' in obj:
                # This is a new Student to create
                json_to_model(model=Student, obj=obj, keys=self.post_keys, model_inst=student)

                students.append(student)
            else:
                student.id = obj['id']

            ordered_students.append(student)

        db.session.bulk_save_objects(students, return_defaults=True)

        # Association list
        class_students = []

        for student in ordered_students:
            if hasattr(student, 'class_id'):
                class_student = ClassStudent(student_id=student.id, class_id=student.class_id)
                student.class_student = class_student
                class_students.append(class_student)

        if class_students:
            db.session.bulk_save_objects(class_students, return_defaults=True)

            # Instantiate Attendance and Assignments


            class_student_ids = [class_student.id for class_student in class_students]
            assignments = []
            attendances = []

            class_homeworks = db.session.query(ClassHomework).filter(ClassHomework.class_id.in_(class_student_ids)).all()
            class_lectures = db.session.query(ClassLecture).filter(ClassLecture.class_id.in_(class_student_ids)).all()

            # Minimize N^2 damage with this
            class_homeworks_map, class_lectures_map = defaultdict(list), defaultdict(list)
            for class_homework in class_homeworks:
                class_homeworks_map[class_homework.class_id].append(class_homework)
            for class_lecture in class_lectures:
                class_lectures_map[class_lecture.class_id].append(class_lecture)


            for class_student in class_students:
                for class_homework in class_homeworks_map[class_student.class_id]:
                    assignments.append(Assignment(class_homework_id=class_homework.id,
                                                  class_student_id=class_student.id))

                for class_lecture in class_lectures_map[class_student.class_id]:
                    attendances.append(Attendance(class_lecture_id=class_lecture.id,
                                                  class_student_id=class_student.id))

            db.session.bulk_save_objects(assignments, return_defaults=False)
            db.session.bulk_save_objects(attendances, return_defaults=False)

        # Prepare response
        rets = []
        for student in ordered_students:
            ret = student.json
            if hasattr(student, 'class_id'):
                ret['class_id'] = student.class_student.class_id
                ret['class_student_id'] = student.class_student.id

            rets.append(ret)

        db.session.commit()

        return jsonify({"meta": {"len": len(rets)}, "data": rets})







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
    post_keys = ['name', 'description']

    @try_except
    def index(self):
        course_id, class_id = parse_id_from_query_args(['course_id', 'class_id'])

        if course_id and class_id:
            raise UserError("Both course_id and class_id cannot be specified simutaneously")

        rets = []
        if course_id:
            q = db.session.query(Lecture, CourseLecture).join(CourseLecture).filter(CourseLecture.course_id == course_id)
            for lecture, course_lecture in q:
                obj = lecture.json
                obj['course_lecture_id'] = course_lecture.id
                rets.append(obj)

        elif class_id:
            q = db.session.query(Lecture, ClassLecture).join(ClassLecture).filter(ClassLecture.class_id == class_id)
            for lecture, class_lecture in q:
                obj = lecture.json
                cl = class_lecture.json  # I have to do this or the date formatting is odd
                obj['class_lecture_id'] = class_lecture.id
                obj['dt'] = cl['dt']
                rets.append(obj)

        else:
            q = db.session.query(Lecture)
            rets = [lecture.json for lecture in q]

        return jsonify({"meta": {"len": len(rets)}, "data": rets})

    @try_except
    @route('/<int:id>/', methods=['GET'])
    def get(self, id=None):
        get_course, get_class = parse_data_from_query_args(['course', 'class'])

        try:
            lecture = db.session.query(Lecture).filter_by(id=id).one()
        except NoResultFound:
            raise UserError("No lecture with id={}".format(id))

        ret = lecture.json

        if get_course:
            ret['courses'] = []
            q = db.session.query(Course, CourseLecture).join(CourseLecture).filter(CourseLecture.lecture_id == id)
            for course, course_lecture in q:
                obj = course.json
                obj['course_lecture_id'] = course_lecture.id
                ret['courses'].append(obj)

        if get_class:
            ret['classes'] = []
            q = db.session.query(Class, ClassLecture).join(ClassLecture).filter(ClassLecture.lecture_id == id)
            for clazz, class_lecture in q:
                obj = clazz.json
                cl = class_lecture.json
                obj['class_lecture_id'] = class_lecture.id
                obj['dt'] = cl['dt']
                ret['classes'].append(obj)

        return jsonify({"meta": {}, "data": ret}), 200




    @try_except
    def put(self):
        raise NotImplementedError("noob copy HomeworkView:post")

    @try_except
    def post(self):
        data = extract_data()

        # This ensures order of the response is indetical to the request
        ordered_lectures = []

        # This contains the new Lectures to create (where "id" is not present)
        lectures = []

        # Check each object in the request, determine if it is New and/or needs to be assocaited to Course/Class
        for obj in data:
            lecture = Lecture()

            if 'course_id' in obj:
                lecture.course_id = obj['course_id']

            if 'class_id' in obj:
                lecture.class_id = obj['class_id']
                if 'dt' not in obj:
                        raise UserError("Class Lectures must have a dt attribute")
                lecture.dt = obj['dt']

            if not 'id' in obj:
                # This is a new Lecture to create
                keys = self.post_keys[:]
                # Class Lectures require a dt, whereas Course lectures do not.
                # ?? Do I need to enforce this?

                json_to_model(model=Lecture, obj=obj, keys=keys, model_inst=lecture)
                #lecture.name = obj['name']
                #lecture.description = obj['description']
                #lecture.dt = datetime.strptime(date_format, obj['dt'])

                lectures.append(lecture)
            else:
                # This is a previous lecture probably to associate
                # Not sure if I should throw in error if 'course_id' or 'class_id' isn't present
                lecture.id = obj['id']

            ordered_lectures.append(lecture)

        # Save only the newly created Lecture
        db.session.bulk_save_objects(lectures, return_defaults=True)

        ## Association lists
        course_lectures = []
        class_lectures = []

        # Check each lecture and determine if it needs to be associated
        for lecture in ordered_lectures:
            if hasattr(lecture, 'course_id'):
                course_lecture = CourseLecture(lecture_id=lecture.id, course_id=lecture.course_id)
                lecture.course_lecture = course_lecture
                course_lectures.append(course_lecture)

            if hasattr(lecture, 'class_id'):
                class_lecture = ClassLecture(lecture_id=lecture.id, class_id=lecture.class_id)
                obj = {'dt': lecture.dt}
                class_lecture = json_to_model(model=ClassLecture, obj=obj, keys=obj.keys(), model_inst=class_lecture)
                lecture.class_lecture = class_lecture
                class_lectures.append(class_lecture)

        if course_lectures:
            for course_lecture in course_lectures:
                app.logger.debug(course_lecture.json)
            db.session.bulk_save_objects(course_lectures, return_defaults=True)

        if class_lectures:
            db.session.bulk_save_objects(class_lectures, return_defaults=True)

            # Instantiate all of the Attendance
            class_lecture_ids = [class_lecture.id for class_lecture in class_lectures]

            # Minimize harm from N^2 loop
            class_lectures_maps = defaultdict(list)
            for class_lecture in class_lectures:
                class_lectures_maps[class_lecture.class_id].append(class_lecture)

            class_students = db.session.query(ClassStudent).filter(ClassStudent.class_id.in_(class_lecture_ids)).all()
            if class_students:
                attendances = []

                for class_student in class_students:
                    for class_lecture in class_lectures_maps[class_student.class_id]:
                        attendances.append(Attendance(class_lecture_id=class_lecture.id,
                                                      class_student_id=class_student.id))

                db.session.bulk_save_objects(attendances, return_defaults=False)

        # Prepare response
        rets = []
        for lecture in ordered_lectures:
            ret = lecture.json

            if hasattr(lecture, 'course_lecture'):
                ret['course_lecture_id'] = lecture.course_lecture.id
                ret['course_id'] = lecture.course_lecture.course_id

            if hasattr(lecture, 'class_lecture'):
                ret['class_lecture_id'] = lecture.class_lecture.id
                ret['class_id'] = lecture.class_lecture.class_id

            rets.append(ret)

        db.session.commit()

        return jsonify({"meta": {"len": len(rets)}, "data": rets})


    @try_except
    def delete(self):
        data = extract_data()

        lecture_ids = []
        course_lectures = []
        class_lectures = []

        for lecture in data:
            if 'course_id' not in lecture and 'class_id' not in lecture:
                lecture_ids.append(lecture['id'])
            else:
                if 'course_id' in lecture:
                    pass

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

    @try_except
    def index(self):
        course_id, class_id = parse_id_from_query_args(['course_id', 'class_id'])

        if course_id and class_id:
            # Should this be the correct behavior?
            raise UserError("course_id and class_id both cannot be requested")

        rets = []

        if course_id:
            q = db.session.query(Homework, CourseHomework).join(CourseHomework).filter(CourseHomework.course_id == course_id)
            for homework, course_homework in q:
                obj = homework.json
                obj['course_homework_id'] = course_homework.id
                rets.append(obj)

        elif class_id:
            q = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.class_id == class_id)
            for homework, class_homework in q:
                obj = homework.json
                obj['class_homework_id'] = class_homework.id
                rets.append(obj)

        else:
            q = db.session.query(Homework)
            rets = [homework.json for homework in q]


        return jsonify({"meta": {"len": len(rets)}, "data": rets})


    @try_except
    @route('/<int:id>/', methods=['GET'])
    def get(self, id=None):
        get_course, get_class = parse_data_from_query_args(['course', 'class'])

        try:
            homework = db.session.query(Homework).filter_by(id=id).one()
        except NoResultFound:
            raise UserError("No homework with id={}".format(id))

        ret = homework.json

        if get_course:
            ret['courses'] = []
            q = db.session.query(Course, CourseHomework).join(CourseHomework).filter(CourseHomework.homework_id == id)
            for course, course_homework in q:
                obj = course.json
                obj['course_homework_id'] = course_homework.id
                ret['courses'].append(obj)

        if get_class:
            ret['classes'] = []
            q = db.session.query(Class, ClassHomework).join(ClassHomework).filter(ClassHomework.homework_id == id)
            for clazz, class_homework in q:
                obj = clazz.json
                obj['class_homework_id'] = class_homework.id
                ret['classes'].append(obj)

        return jsonify({"meta": {}, "data": ret}), 200

    @try_except
    def put(self):
        '''
        When a Class is created, the Class Homework and Class Lectures are automatically instantiated
        from the Course Homework and Course Lectures for this class.course_id.

        The teacher can change a particular homework to suite his needs for that particular class.

        On the backend, what actually happens is the following:
            If teacher modifies the Class Homework for the first time
                A new Homwork is created, containing the same name, content, and etc. as the original Homework.
                    The parent_id of this Homework is set to the id of the original Homework.
                    The new Homwork's name, content and etc. are set to what the teacher proposes
            If teacher modifies a previously modified Class Homework:
                None of the above happens
                The modified Homework gets modified again

        I need to think about how I'm going to differentiate these three use cases especially regarding the URIs:
            Admin changes the Course level template Homework
                Maybe just if the ID is passed in?
            Teacher changes the Class level instance Homework for the first time
                Maybe just if the class_lecture_id is passed in?
            Teacher changes a previously changed class level instance homework
                Either the ID or the class_lecture_id is passed in?

        '''




        ## OK Let's try it this way
        ## If id AND class_homework_id are present, teacher is changing the class level
        ## If only ID is present, admin is changing the course level

        data = extract_data()
        admin_homework_objs = []
        teacher_homework_objs = []

        for obj in data:
            if 'class_homework_id' not in obj:
                admin_homework_objs.append(obj)
            else:
                teacher_homework_objs.append(obj)

        # Get all the Homework objs for the teacher homeworks
        ids = [obj['class_homework_id'] for obj in teacher_homework_objs]

        q = db.session.query(Homework).join(ClassHomework).filter(ClassHomework.id._in(ids))
        for homework in g:
            pass





















        data = extract_data()

        admin_homework_objs = []
        teacher_homework_objs = {}

        for obj in data:
            if 'id' in obj:
                # Admin is modifying Course Homework
                admin_homework_objs.append(obj)
            elif 'class_homework_id' in obj:
                # Teacher is modifying Class Homework
                teacher_homework_objs[obj['class_homework_id']] = obj
            else:
                raise UserError("expecting either id or class_homework_id - not in {}".format(obj))

        bulk_update(Homework, admin_homework_objs)

        # How do we determine if teacher is modifying the homework for the first time or not?
        # I suppose if parent_id is null, then its the first time that it was modified ...
        teacher_class_homework_ids = [obj['class_homework_id'] for obj in teacher_homework_objs.keys()]
        if teacher_class_homework_ids:
            # Query all the Homeworks on these class homework ids
            homeworks = db.session.query(Homework, ClassHomework).join(ClassHomework).filter(ClassHomework.id.in_(teacher_class_homework_ids))

            # These two arrays will have corresponding indexes for the Homework- ClassHomework joined on OLD homework.id
            teacher_homeworks = []
            teacher_class_homeworks = []

            for homework, class_homework in homeworks:
                new_homework_obj = teacher_homework_objs[class_homework.id]

                if homework.parent_id is None:
                    # Teacher is modifying a homework for the first time
                    parent_id = homework.id
                    # Clone the homeworks
                    db.session.expunge(homework)
                    make_transient(homework)
                    # Set clone'd homework's parent Id to originals
                    homework.id = None
                    homework.parent_id = parent_id

                    teacher_homeworks.append(homework)
                    teacher_class_homeworks.append(class_homework)

                homework.name = new_homework_obj['name']

                # Keep track of the homework and class_homework



            db.session.bulk_save_objects(teacher_homeworks, return_defaults=True)

            count = 0
            for homework in teacher_homeworks:
                class_homework = teacher_class_homeworks[count]
                class_homework.homework_id = homework.id
                count += 1



        #db.session.bulk_save_objects(teacher_class_homeworks)


    @try_except
    def post(self):
        '''
        /api/homework handles multiple operations, which can be mixed and matched in the same request
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

        For example, a request containing each of those 5 operations, in order, would look like this:
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

        This API will perform all the operations and return the following response:
            {
                "data": [
                    {
                       "id": 1, "name": "Python Metaclasses"
                    },
                    {
                       "id": 2, "name": "Python variables", "course_homework_id": 500, "course_id": 1
                    },
                    {
                       "name": "Python loops", "class_homework_id": 1001, "class_id": 10
                    },
                    {
                       "id": 1, "course_homework_id": 501, "course_id": 1, "name": ""
                    },
                    {
                       "id": 1, "class_homework_id": 1002, ""class_id": 10, name": ""
                    },
                ]
            }

        Note how the response is returned in the exact same order as the Request

        Note how "id"s have been added to the newly created Homeworks

        Note how "course_homework_id" and "class_homework_id" are added to those that were associated accordingly

        Note how "name" is empty for cases 4 and 5.
        '''


        #app.logger.debug(" IN HOMEWORK YO")
        data = extract_data()

        # To ensure the order of the response is identical to the request, use this array
        ordered_homeworks = []

        # This contains the new Homeworks to create (where "id" is not present")
        homeworks = []

        # Check each object in the request, determine if it is New and/or if it needs to be associated to Course/Class
        for obj in data:
            homework = Homework()

            if 'course_id' in obj:
                homework.course_id = obj['course_id']

            if 'class_id' in obj:
                homework.class_id = obj['class_id']

            if not 'id' in obj:
                # This is a new Homework to create
                json_to_model(model=Homework, obj=obj, keys=self.post_keys, model_inst=homework)
                #homework.name = obj['name']

                homeworks.append(homework)
                ordered_homeworks.append(homework)
            else:
                # This is a previous Homework probably to associate
                # Not sure if I should throw an error if 'course_id' or 'class_id' isn't present as it's a mistake
                homework.id = obj['id']
                ordered_homeworks.append(homework)

        # This only saves the newly created Homeworks
        db.session.bulk_save_objects(homeworks, return_defaults=True)

        # Association lists
        course_homeworks = []
        class_homeworks = []

        # Check each homework and determine if it needs to be associated
        for homework in ordered_homeworks:
            if hasattr(homework, 'course_id'):
                course_homework = CourseHomework(homework_id=homework.id, course_id=homework.course_id)
                homework.course_homework = course_homework
                course_homeworks.append(course_homework)
            if hasattr(homework, 'class_id'):
                class_homework = ClassHomework(homework_id=homework.id, class_id=homework.class_id)
                homework.class_homework = class_homework
                class_homeworks.append(class_homework)

        if course_homeworks:
            db.session.bulk_save_objects(course_homeworks, return_defaults=True)

        if class_homeworks:
            db.session.bulk_save_objects(class_homeworks, return_defaults=True)

            class_homework_ids = [class_homework.id for class_homework in class_homeworks]

            # Minimize harm from N^2 loop
            class_homeworks_map = defaultdict(list)
            for class_homework in class_homeworks:
                class_homeworks_map[class_homework.class_id].append(class_homework)

            class_students = db.session.query(ClassStudent).filter(ClassStudent.class_id.in_(class_homework_ids)).all()
            if class_students:
                assignments = []

                for class_student in class_students:
                    for class_homework in class_homeworks_map[class_student['class_id']]:
                        assignments.append(Assignment(class_homework_id=class_homework.id,
                                                      class_student_id=class_student.id))

                db.session.bulk_save_objects(assignments, return_defaults=False)

        # Prepare response
        rets = []
        for homework in ordered_homeworks:
            lol = homework.json
            if hasattr(homework, 'course_homework'):
                # Attach the course_homework related information if necessary
                lol['course_homework_id'] = homework.course_homework.id
                lol['course_id'] = homework.course_homework.course_id
            if hasattr(homework, 'class_homework'):
                # Attach the class_homework related information if necessary
                lol['class_homework_id'] = homework.class_homework.id
                lol['class_id'] = homework.class_homework.class_id

            rets.append(lol)

        db.session.commit()

        return jsonify({"meta": {"len": len(homeworks)}, "data": rets}), 200


class AssignmentView(BaseView):
    model = Assignment
    post_keys = ['class_student_id', 'class_homework_id', 'did_complete']
    @try_except
    def index(self):
        class_homework_id, class_student_id, class_id, student_id = parse_id_from_query_args(
            ['class_homework_id', 'class_student_id', 'class_id', 'student_id']
        )

        # Should I just put this logic in parse_id_from_query_args
        if sum([class_homework_id, class_student_id, class_id, student_id]) not in [class_homework_id, class_student_id,
                                                                                    class_id, student_id]:
            raise UserError("Only one of class_homework_id, class_student_id, class_id, or student_id can be filtered")

        rets = []

        q = db.session.query(Homework, Assignment, Student, Class)
        q = q.join(ClassHomework).join(Assignment).join(ClassStudent).join(Student).join(Class, ClassStudent.class_id==Class.id)

        if class_homework_id:
            q = q.filter(ClassHomework.id == class_homework_id)

        elif class_student_id:
            q = q.filter(ClassStudent.id == class_student_id)

        elif class_id:
            # Get the Class as well
            q = q.filter(Class.id == class_id)

        elif student_id:
            q = q.filter(Student.id == student_id)

        for homework, assignment, student, clazz in q:
                obj = assignment.json
                obj['homework'] = homework.json
                obj['student'] = student.json
                obj['class'] = clazz.json

                rets.append(obj)

        return jsonify({"meta": {"len": len(rets)}, "data": rets}), 200

    ## I dont see a need for a custom get(/id/) for Assignment
    # The teacher will go to Course, then to ClassHomework, then query /assigntment/?class_homework_id=1

    @try_except
    def post(self):
        raise UserError("Assignment creation is not supported. Create a Homework and add to a Class to instantiate an Assignment")

    @try_except
    def delete(self):
        raise UserError("Assignments cannot be deleted this way. Either delete the student or delete the ClassHomework")


class AttendanceView(BaseView):
    model = Attendance
    post_keys = ['class_lecture_id', 'class_student_id', 'did_attend']

    @try_except
    def index(self):
        class_lecture_id, class_student_id, class_id, student_id = parse_id_from_query_args(
            ['class_lecture_id', 'class_student_id', 'class_id', 'student_id']
        )

        # Should I just put this logic in parse_id_from_query_args ?
        if sum([class_lecture_id, class_student_id, class_id, student_id]) not in [class_lecture_id, class_student_id,
                                                                                     class_id, student_id]:
            raise UserError("Only one of class_lecture_id, class_student_id, class_id, or student_id can be used to filter")

        rets = []

        q = db.session.query(Lecture, Attendance, Student, Class)
        q = q.join(ClassLecture).join(Attendance).join(ClassStudent).join(Student).join(Class, ClassStudent.class_id == Class.id)

        if class_lecture_id:
            q = q.filter(ClassLecture.id == class_lecture_id)

        elif class_student_id:
            q = q.filter(ClassStudent.id == class_student_id)

        elif class_id:
            q = q.filter(Class.id == class_id)

        elif student_id:
            q = q.filter(Student.id == student_id)

        for lecture, attendance, student, clazz in q:
            obj = attendance.json
            obj['lecture'] = lecture.json
            obj['student'] = student.json
            obj['class'] = clazz.json

            rets.append(obj)

        return jsonify({"meta": {"len": len(rets)}, "data": rets})

    @try_except
    def post(self):
        raise UserError("Attendance creation is not supported. Create a Lecture and add to a Class to instantiate an Attendance")

    @try_except
    def delete(self):
        raise UserError("Attendances cannot be deleted this way. Either delete the student or delete the ClassHomework")

'''
class AttendanceView(BaseView):
    model = Attendance
    post_keys = ['lecture_id', 'class_student_id', 'did_attend']

class AssignmentView(BaseView):
    model = Assignment
    post_keys = ['class_student_id', 'course_homework_id', 'is_completed']
'''

views = [CourseView, ClassView, StudentView, LectureView, HomeworkView, AssignmentView, AttendanceView]
for view in views:
    view.register(app, route_prefix='/api/', trailing_slash=True)
