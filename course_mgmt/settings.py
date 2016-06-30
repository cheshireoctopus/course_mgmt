import os

DATABASE_CONNECTION = 'postgresql://postgres:postgres@localhost/course_mgmt'
DEBUG = True
LEGAL_DATABASES = ['sqlite', 'postgresql']
BASE_URL = 'http://localhost:5000/'

class ConfigBase(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'abc123'
    #SESSION_COOKIE_SECURE = True


class Config(ConfigBase):
    SQLALCHEMY_DATABASE_URI = os.environ.get('COURSE_MGMT_DATABASE', DATABASE_CONNECTION)
    DEBUG = os.environ.get('COURSE_MGMT_DEBUG', DEBUG)
    BASE_URL = os.environ.get('COURSE_MGMT_BASE_URI', BASE_URL)
    GITHUB_CLIENT_ID = os.environ.get('COURSE_MGMT_GITHUB_CLIENT_ID', None)
    GITHUB_CLIENT_SECRET = os.environ.get('COURSE_MGMT_GITHUB_CLIENT_SECRET', None)
    GITHUB_REDIRECT_URL = os.environ.get('COURSE_MGMT_GITHUB_REDIRECT_URL', None)


try:
    from course_mgmt.local_settings import *
except:
    pass