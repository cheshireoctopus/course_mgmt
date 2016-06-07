__author__ = 'mmoisen'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask import render_template
import markdown
from flask import Markup
import os

# Sqlite doesn't enforce Foreign Keys by default. This enables it
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Set static assets path
app = Flask(__name__, static_folder='front_end/build', static_url_path='/static')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

db = SQLAlchemy(app)

sqlite_path = 'sqlite:///db.db'

app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path

# Secret key is required for CSR stuff change this to something more secure
app.secret_key = 'abc123'

# Routes
@app.route('/')
def index():
    return render_template('index.jade', data={'app': 'courses'})

@app.route('/class/')
def classes():
    return render_template('index.jade', data={'app': 'classes'})

@app.route('/docs/', defaults={'path': None})
@app.route('/docs/<path:path>/')
def doc(path):
    if path is None:
        path = 'SUMMARY.md'

    p = os.path.abspath(os.path.join('docs', path))

    with open(p) as f:
        content = f.readlines()

    content = u''.join(content)

    content = Markup(markdown.markdown(content))

    app.logger.debug("content is {}".format(content))

    return render_template('docs.html', content=content)


# TODO enable this better
try:
    from local_settings import opbeat
except ImportError:
    pass

from views import *

