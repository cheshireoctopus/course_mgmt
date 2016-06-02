__author__ = 'mmoisen'
from course_mgmt import app
from course_mgmt import db
from course_mgmt.views import ServerError
from datetime import datetime
date_format = '%Y-%m-%d %H:%M:%S'
from sqlalchemy.sql.sqltypes import Date, DateTime


def to_json(inst, cls):
    """
    Convert a SQLAlchemy query result into a serializable dict.
    http://stackoverflow.com/a/9746249/1391717

    I ended up changing this a bit because I couldn't get it to work with DateTimes.


    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    convert[Date] = lambda dt: dt.strftime(date_format)
    convert[DateTime] = lambda dt: dt.strftime(date_format)
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if type(c.type) in convert.keys() and v is not None:
            try:
                d[c.name] = convert[type(c.type)](v)
            except Exception as ex:
                app.logger.exception("Failed to convert: {}".format(ex.message))
                raise ServerError("Failed to convert: {}".format(ex.message))
                #[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d



class BaseModel(db.Model):
    '''
    All Models should extend the Base model so that they can implement the json method
    '''
    __abstract__ = True

    @property
    def json(self):
        return to_json(self, self.__class__)

class Course(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    classes = db.relationship('Class', backref=db.backref('course'))

    plural = 'course'

class Class(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('course_id', 'start_dt', 'end_dt'),)

    plural = 'class'


class Student(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    github_username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String)

    plural = 'student'


class ClassStudent(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('class_id', 'student_id'),)


class Lecture(BaseModel):
    '''
    This could probably be associated to the course level just like homework is ...
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    dt = db.Column(db.DateTime)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    plural = 'lecture'





class Attendance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id'), nullable=False)
    did_attend = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (db.UniqueConstraint('lecture_id', 'class_student_id'),
                      # Index it both way (e.g., include student_id, lecture_id) as per the access patterns
                      )



class Homework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    plural = 'homework'


class CourseHomework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('course_id', 'homework_id'),)

class Assignment(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id'), nullable=False)
    course_homework_id = db.Column(db.Integer, db.ForeignKey('course_homework.id'), nullable=False)
    is_completed = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('class_student_id', 'course_homework_id'),)

    plural = 'assignment'


all_models = [Student, Lecture, Homework]