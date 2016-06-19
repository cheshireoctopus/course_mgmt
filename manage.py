from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from course_mgmt import app, db


# Read Flask Migrate tutorial by author here
# http://blog.miguelgrinberg.com/post/flask-migrate-alembic-database-migration-wrapper-for-flask

# Normal use: python manage.py db migrate

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

