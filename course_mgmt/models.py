__author__ = 'mmoisen'
from course_mgmt import app
from course_mgmt import db
from course_mgmt.views import ServerError, date_format
from datetime import datetime
#date_format = '%Y-%m-%d %H:%M:%S'
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.orm import validates
from course_mgmt.views import UserError

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
            d[c.name] = None
        else:
            d[c.name] = v
    return d


'''
In shell for testing:

from course_mgmt import app, db
from course_mgmt.models import *
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

course = Course(name='')
db.session.add(course)
try:
    db.session.commit()
except IntegrityError as ex:
    print ex.message

db.session.rollback()

class SqliteSequence(db.Model):
    __tablename__ = 'sqlite_sequence'
    name = db.Column(db.String, primary_key=True)
    seq = db.Column(db.Integer)

course = db.session.query(SqliteSequence).filter_by(name='course').one()

class Hello(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    __table_args__ = (db.UniqueConstraint('name'), {'sqlite_autoincrement': True})


db.create_all()
'''


class BaseModel(db.Model):
    '''
    All Models should extend the Base model so that they can implement the json method
    '''
    __abstract__ = True

    @property
    def json(self):
        return to_json(self, self.__class__)


class Teacher(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Course(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    classes = db.relationship('Class', backref=db.backref('course'))

    __table_args__ = (db.CheckConstraint("name <> ''"), {'sqlite_autoincrement': True})


class Class(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('course_id', 'name'),
                      db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True})



class Student(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    github_username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String)

    __table_args__ = (db.CheckConstraint("first_name <> ''"),
                      db.CheckConstraint("last_name <> ''"),
                      db.CheckConstraint("github_username <> ''"),
                      db.CheckConstraint("email <> ''"),
                      db.CheckConstraint("photo_url <> ''"),
                      {'sqlite_autoincrement': True})


class Lecture(BaseModel):
    '''
    This could probably be associated to the course level just like homework is ...
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                       {'sqlite_autoincrement': True})


class ClassStudent(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('class_id', 'student_id'), {'sqlite_autoincrement': True})



class Homework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # A Homework can be dervived from another homework
    # This is the case when a Class Homework is modified from the usual course homework
    parent_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True})


class CourseHomework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id', ondelete='CASCADE'), nullable=False)
    course_lecture_id = db.Column(db.Integer, db.ForeignKey('course_lecture.id', ondelete='SET NULL'), nullable=True)

    __table_args__ = (db.UniqueConstraint('course_id', 'homework_id'), {'sqlite_autoincrement': True})

class ClassHomework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id', ondelete='CASCADE'), nullable=False)
    class_lecture_id = db.Column(db.Integer, db.ForeignKey('class_lecture.id', ondelete='SET NULL'), nullable=True)

    __table_args__ = (db.UniqueConstraint('class_id', 'homework_id'), {'sqlite_autoincrement': True})


class CourseLecture(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('course_id', 'lecture_id'), {'sqlite_autoincrement': True})

class ClassLecture(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id', ondelete='CASCADE'), nullable=False)
    dt = db.Column(db.DateTime, nullable=True)  # nullable because it will instantiate as null

    __table_args__ = (db.UniqueConstraint('class_id', 'lecture_id'), {'sqlite_autoincrement': True})


class Assignment(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id', ondelete='CASCADE'), nullable=False)
    class_homework_id = db.Column(db.Integer, db.ForeignKey('class_homework.id', ondelete='CASCADE'), nullable=False)
    is_completed = db.Column(db.Boolean)

    __table_args__ = (db.UniqueConstraint('class_student_id', 'class_homework_id'), {'sqlite_autoincrement': True})

class Attendance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_lecture_id = db.Column(db.Integer, db.ForeignKey('class_lecture.id', ondelete='CASCADE'), nullable=False)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id', ondelete='CASCADE'), nullable=False)
    did_attend = db.Column(db.Boolean)

    __table_args__ = (db.UniqueConstraint('class_lecture_id', 'class_student_id'), {'sqlite_autoincrement': True},
                      # TODO ? Index it both ways (e.g., include student_id, lecture_id) as per the access patterns
                      )

all_models = [ClassStudent, Attendance, Assignment, ClassHomework, ClassLecture,
              CourseHomework, CourseLecture, Class, Student, Homework, Lecture, Course]