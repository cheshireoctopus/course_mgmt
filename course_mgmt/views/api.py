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
    post_keys = ['start_dt', 'end_dt', 'course_id']

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
            data = request.json['data']

        if not isinstance(data, list):
            raise UserError({"data attribute should be dict/json"})

        ## Create Class
        clazzes = bulk_save(self.model, data, self.post_keys)

        class_ids = [clazz.id for clazz in clazzes]

        ## Instantiate ClassHomework from CourseHomework
        course_homeworks = db.session.query(CourseHomework).filter(CourseHomework.course_id.in_(class_ids)).all()
        data = [{'class_id': clazz.id, 'homework_id': course_homework.id} for course_homework in course_homeworks]
        class_homeworks = bulk_save(ClassHomework, data, ['class_id', 'homework_id'])

        ## Instantiate ClassLecture from CourseLecture
        course_lectures = db.session.query(CourseLecture).filter(CourseLecture.course_id.in_(class_ids)).all()
        data = [{'class_id': clazz.id, 'lecture_id': course_lecture.id} for course_lecture in course_lectures]
        class_lectures = bulk_save(ClassLecture, data, ['class_id', 'lecture_id'])

        clazzes = [clazz.json for clazz in clazzes]

        db.session.commit()

        return jsonify({"meta": {"len": len(clazzes)}, "data": clazzes})




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

        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

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
    post_keys = ['name', 'description', 'dt']

    @try_except
    def post(self):
        form = request.json
        keys = 'data'
        data = extract_form(form, keys)

        # Step 1, loop over data and distringuish between
        #   New Foos to Insert
        #       No "id" key
        #   New Foos to Insert and Associate with Bars
        #       No "Id" key, but "bar_id" key present
        #   Old Foos to Associate with Bars
        #       "id" key AND "bar_id" key present


        ##############################################
        # Second attempt




        ##############################################
        # First attempt
        # Identify New Foos to insert
        lectures = []
        course_lectures = []
        class_lectures = []

        new_lectures = []
        for obj in data:
            if 'id' not in obj:
                new_lectures.append(obj)

        # This returns lectures with an "obj" attribute that may or may not contain
        # any course_id or class_id
        lectures = bulk_save(Lecture, new_lectures, self.post_keys)

        # Prepare course_lecture_objs
        course_lecture_objs = [{'course_id': lecture.obj['course_id'], 'lecture_id': lecture.id}
                               for lecture in lectures if 'course_id' in lecture.obj]

        # Add old lectures from data that are not in lectures
        course_lecture_objs.extend([{'course_id': lecture['course_id'], 'lecture_id': lecture['id']}
                                for lecture in data if 'id' in lecture])

        if course_lecture_objs:
            course_lectures = bulk_save(CourseLecture, course_lecture_objs, ['course_id', 'lecture_id'])

        # Prepare class_lecture_objs
        class_lecture_objs = [{'class_id': lecture.obj['class_id'], 'lecture_id': lecture.id}
                              for lecture in lectures if 'class_id' in lecture.obj]

        # Add old lectures from data that are not in lectures
        class_lecture_objs.extend([{'class_id': lecture['class_id'], 'lecture_id': lecture['id']}
                              for lecture in data if 'id' in lecture])

        if class_lecture_objs:
            class_lectures = bulk_save(ClassLecture, class_lecture_objs, ['class_id', 'lecture_id'])

        ret = lectures + course_lectures + class_lectures

        ret = [r.json for r in ret]

        db.session.commit()

        return jsonify({"meta": {"len": len(lectures)}, "data": ret})

        ### WTF do I return???
        # If I just return lectures, that is only the newly created lectures, and doesn't include the
        # class_lecture_id or course_lecture_id
        lectures = bulk_save(Lecture, data, self.post_keys)




        ########################
        # OLD

        # Add Lectures to Courses if course_id specified
        course_lecture_objs = [{'course_id': lecture.obj['course_id'], 'lecture_id': lecture.id}
                               for lecture in lectures if 'course_id' in lecture.obj]
        if course_lecture_objs:
            bulk_save(CourseLecture, course_lecture_objs, ['course_id', 'lecture_id'])

        # Add Lectures to Classes if class_id specified
        class_lecture_objs = [{'class_id': lecture.obj['class_id'], 'lecture_id': lecture.id}
                              for lecture in lectures if 'class_id' in lecture.obj]
        if class_lecture_objs:
            bulk_save(ClassLecture, class_lecture_objs, ['class_id', 'lecture_id'])

        lectures = [lecture.json for lecture in lectures]

        db.session.commit()

        return jsonify({"meta": {"len": len(lectures)}, "data": lectures})

    @try_except
    def delete(self):
        data = request.json['data']

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
        data = request.json['data']

        # To ensure the order of the response is identical as 
        ordered_homeworks = []
        homeworks = []
        for obj in data:
            homework = Homework()  # Homework(name=obj['name'])
            if 'course_id' in obj:
                homework.course_id = obj['course_id']
            if 'class_id' in obj:
                homework.class_id = obj['class_id']
            if not 'id' in obj:
                homework.name = obj['name']
                homeworks.append(homework)
                ordered_homeworks.append(homework)
            else:
                homework.id = obj['id']
                ordered_homeworks.append(homework)

        db.session.bulk_save_objects(homeworks, return_defaults=True)

        course_homeworks = []
        class_homeworks = []

        for homework in ordered_homeworks: #  homeworks:
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

            # TODO Instantiate all the Assignments

        rets = []
        for homework in ordered_homeworks:
            lol = homework.json
            if hasattr(homework, 'course_homework'):
                lol['course_homework_id'] = homework.course_homework.id
                lol['course_id'] = homework.course_homework.course_id
            if hasattr(homework, 'class_homework'):
                lol['class_homework_id'] = homework.class_homework.id
                lol['class_id'] = homework.class_homework.class_id

            rets.append(lol)

        db.session.commit()

        return jsonify({"meta": {"len": len(homeworks)}, "data": rets}), 200

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
