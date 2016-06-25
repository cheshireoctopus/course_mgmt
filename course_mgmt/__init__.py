__author__ = 'mmoisen'
from flask import Flask
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


# Routes
@app.route('/')
def index():
    return render_template('index.jade', data={'app': 'courses'})

@app.route('/class/')
def classes():
    return render_template('index.jade', data={'app': 'classes'})

@app.route('/student/')
def students():
    return render_template('index.jade', data={'app': 'students'})

from course_mgmt.views import *

