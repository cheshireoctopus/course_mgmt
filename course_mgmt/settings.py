import os

DATABASE_CONNECTION = 'postgresql://postgres:postgres@localhost/course_mgmt'
DEBUG = True
LEGAL_DATABASES = ['sqlite', 'postgresql']

class ConfigBase(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'abc123'


class Config(ConfigBase):
    SQLALCHEMY_DATABASE_URI = os.environ.get('COURSE_MGMT_DATABASE', DATABASE_CONNECTION)
    DEBUG = os.environ.get('COURSE_MGMT_DEBUG', DEBUG)


try:
    from course_mgmt.local_settings import *
except:
    pass