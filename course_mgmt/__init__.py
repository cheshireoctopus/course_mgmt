__author__ = 'mmoisen'
from flask import Flask, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask import render_template
from settings import Config, LEGAL_DATABASES


def parse_database_from_uri(database_uri):
    if '+' in database_uri:
        split = '+'
    elif ':' in database_uri:
        split = ':'
    else:
        raise ValueError("Incorrect database connection URI: {}".format(database_uri))

    database = database_uri[:database_uri.find(split)]

    if database not in LEGAL_DATABASES:
        KeyError('Database "{}" not in allowed list {}'.format(database, LEGAL_DATABASES))

    return database

# Set static assets path
app = Flask(__name__, static_folder='front_end/build', static_url_path='/static')
app.config.from_object(Config)
# Secret key is required for CSRF stuff change this to something more secure
app.secret_key = app.config['SECRET_KEY']
app.config['DATABASE'] = parse_database_from_uri(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_ECHO'] = True
app.logger.debug("I am {}".format(app.config['DATABASE']))

if app.config['DATABASE'] == 'sqlite':
    # Sqlite doesn't enforce Foreign Keys by default. This enables it
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

db = SQLAlchemy(app)

# Enable Jade templates
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


# Front end needs to make a login.jade or some how do it with index
def login_required_ui(f):
    @wraps(f)
    def _login_required_ui(*args, **kwargs):
        if not session or not 'logged_in' in session or not session['logged_in']:
            return render_template('login.jade', data={'app': 'courses'})
        return f(*args, **kwargs)

    return _login_required_ui

# Routes
@app.route('/')
@login_required_ui
def index():
    return render_template('index.jade', data={'app': 'courses'})

@login_required_ui
@app.route('/class/')
def classes():
    return render_template('index.jade', data={'app': 'classes'})


from flask import redirect, session
import uuid
import requests

def check_github_disabled():
    github_disabled = False
    if 'GITHUB_CLIENT_ID' not in app.config:
        github_disabled = True
    if 'GITHUB_CLIENT_SECRET' not in app.config:
        github_disabled = True
    if 'GITHUB_REDIRECT_URL' not in app.config:
        github_disabled = True

    if github_disabled:
        raise ServerError("config must contain both GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET to authenticate with github")

@app.route('/login/github/')
def github():
    check_github_disabled()
    session['github_state'] = str(uuid.uuid4())
    params = {
        'client_id': app.config['GITHUB_CLIENT_ID'],
        'redirect_url': app.config['GITHUB_REDIRECT_URL'],
        'state': session['github_state'],
        #'scope': 'user:email'


    }
    params = '?' + '&'.join([key + '=' + val for key, val in params.iteritems()])
    print params
    return redirect('https://github.com/login/oauth/authorize' + params)

@app.route('/login/github/redirect/', methods=['GET', 'POST'])
def github_redirect():
    check_github_disabled()

    if 'github_state' not in session:
        raise UserError("Dont hit this URL directly")

    if 'github_state' in session:
        print "session state is {}".format(session['github_state'])
    else:
        print "state not in session nooob"

    state = request.args.get('state', None)
    code = request.args.get('code', None)

    if not state or not code:
        raise ServerError("state or code not specified")

    if state != session['github_state']:
        raise AuthenticationError("session state does not match github state")

    data = {
        'client_id': app.config['GITHUB_CLIENT_ID'],
        'client_secret': app.config['GITHUB_CLIENT_SECRET'],
        'code': code,
        #'redirect_url': 'lol',
        'state': session['github_state']

    }
    headers = {
        'Accept': 'application/json'
    }
    r = requests.post(url='https://github.com/login/oauth/access_token', json=data, headers=headers)
    print r.json()

    access_token = r.json()['access_token']


    a = requests.get(url='https://api.github.com/user/emails?access_token={}'.format(access_token))
    #a = requests.get(url='https://api.github.com/user?access_token={}'.format(access_token))
    data = a.json()
    email = next(d for d in data if d['primary'])['email']




    return email

from course_mgmt.views import *

