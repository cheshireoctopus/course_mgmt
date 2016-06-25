__author__ = 'mmoisen'
class UserError(Exception):
    pass

class ServerError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'  # '%Y-%m-%d %H:%M:%S'

from api import *