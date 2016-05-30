__author__ = 'mmoisen'
class UserError(Exception):
    pass

class ServerError(Exception):
    pass

from course_mgmt.models import *

from api import *