__author__ = 'mmoisen'
from course_mgmt import app
from course_mgmt import db
from course_mgmt.views import ServerError, date_format
from sqlalchemy.dialects.sqlite import SMALLINT
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


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship('Child', backref=db.backref('parent'))

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foo = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)

'''
from course_mgmt import app, db
from course_mgmt.models import *
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

parent = Parent()
db.session.add(parent)
db.session.commit()

c = Child(foo='hai', parent_id=parent.id)
db.session.add(c)
db.session.commit()

parents = []
children = []

for parent, child in db.session.query(Parent, Child).join(Child):
    parents.append(parent)
    children.append(child)

parents[0].children
children[0].parent


c.parent

q = db.session.query(Child).filter_by(foo='hai')

c = q.one()


print c.parent.statement
c.parent.id
'''

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

is_sqlite = app.config['DATABASE'] == 'sqlite'

class BaseModel(db.Model):
    '''
    All Models should extend the Base model so that they can implement the json method
    '''
    __abstract__ = True

    @property
    def json(self):
        return to_json(self, self.__class__)


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    __table_args__ = (db.CheckConstraint("first_name <> ''"),
                      db.CheckConstraint("last_name <> ''"),
                      db.CheckConstraint("email <> ''"),
                      db.CheckConstraint("password <> ''"),
                      db.CheckConstraint("type in ('teacher', 'student')"),
                      {'sqlite_autoincrement': True})

    post_keys = ['first_name', 'last_name', 'email', 'password', 'type']



class Teacher(BaseModel):
    # SQlite has weird behavior for a primary key as a FK where it tries to autoincrement for Integer but not Smallint
    if is_sqlite:
        id = db.Column(SMALLINT, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    else:
        id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)


class Student(BaseModel):
    # SQlite has weird behavior for a primary key as a FK where it tries to autoincrement for Integer but not Smallint
    if is_sqlite:
        id = db.Column(SMALLINT, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    else:
        id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    github_username = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String)

    __table_args__ = (db.CheckConstraint("github_username <> ''"),
                      db.CheckConstraint("photo_url <> ''"),)

    post_keys = ['github_username', 'photo_url']

class Org(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True},)

    post_keys = ['name']

class Role(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True})

class OrgTeacher(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('org.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    courses = db.relationship('Course', backref=db.backref('org_teacher'))

    __table_args__ = (db.UniqueConstraint('org_id', 'teacher_id'), {'sqlite_autoincrement': True})

class OrgTeacherRole(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    org_teacher_id = db.Column(db.Integer, db.ForeignKey('org_teacher.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('org_teacher_id', 'role_id'), {'sqlite_autoincrement': True})

class ClassStudent(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('class_id', 'student_id'), {'sqlite_autoincrement': True})

class ClassStudentRole(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('class_student_id', 'role_id'), {'sqlite_autoincrement': True})

class Course(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    org_teacher_id = db.Column(db.Integer, db.ForeignKey('org_teacher.id', ondelete='CASCADE'), nullable=False)
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






class Lecture(BaseModel):
    '''
    This could probably be associated to the course level just like homework is ...
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('lecture.id', ondelete='SET NULL'), nullable=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                       {'sqlite_autoincrement': True})



class Tag(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True})

class Homework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # A Homework can be dervived from another homework
    # This is the case when a Class Homework is modified from the usual course homework
    parent_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=True)

    __table_args__ = (db.CheckConstraint("name <> ''"),
                      {'sqlite_autoincrement': True})

class TagHomework(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (db.UniqueConstraint('tag_id', 'homework_id'),
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
    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (db.UniqueConstraint('class_student_id', 'class_homework_id'), {'sqlite_autoincrement': True})

class Attendance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    class_lecture_id = db.Column(db.Integer, db.ForeignKey('class_lecture.id', ondelete='CASCADE'), nullable=False)
    class_student_id = db.Column(db.Integer, db.ForeignKey('class_student.id', ondelete='CASCADE'), nullable=False)
    did_attend = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (db.UniqueConstraint('class_lecture_id', 'class_student_id'), {'sqlite_autoincrement': True},
                      # TODO ? Index it both ways (e.g., include student_id, lecture_id) as per the access patterns
                      )

all_models = [ClassStudent, Attendance, Assignment, ClassHomework, ClassLecture,
              CourseHomework, CourseLecture, Class, Student, Homework, Lecture, OrgTeacher, ClassStudentRole, OrgTeacherRole, Role, Course, Teacher, User]
