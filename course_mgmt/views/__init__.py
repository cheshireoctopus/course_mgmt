__author__ = 'mmoisen'
class UserError(Exception):
    pass

class ServerError(Exception):
    pass

from course_mgmt.models import *

from api import *


from course_mgmt import app
from flask.ext.classy import FlaskView, route

quotes = ['a','b','c']


class AView(FlaskView):
    model = None

    def index(self):
        return self.get(None)

    def get(self, id=None):
        return '{} {}'.format(self.model, id)


class QuotesView(AView):
    model = 'QuoteModel'

    @route('/yo/')
    @route('/yo/<int:id>/')
    def yo(self, id=None):
        return "yo {}".format(id)

QuotesView.register(app)



def bulk_save(model, data, keys):
    '''
    Helper method to bulk save a single parent model
    This does not commit so make sure to do so elsewhere.
    :param model: A parent Model (Course, Student, Homework)
    :param data: A list of dicts
    :param keys: the keys for the dicts, fieldnames for this Model
    :param update: if False, an insert is performed; otherwise an update is performed.
    :return: list of DB objects
    '''
    try:
        # objs = [model(**{key: obj[key] for key in keys}) for obj in data ]
        # Unforunately the above won't work because of date
        # There must be a better way of doing this

        objs = []
        for obj in data:
            kwargs = {}
            for key in keys:
                if isinstance(getattr(model, key).type, DateTime):
                    kwargs[key] = datetime.strptime(obj[key], date_format)
                else:
                    kwargs[key] = obj[key]

                objs.append(model(**kwargs))

    except KeyError as ex:
        raise UserError("Expecting {}".format(keys))

    db.session.bulk_save_objects(objs, return_defaults=True)

    return objs


def bulk_update(model, data):
    objs = []
    for obj in data:
        kwargs = {}
        for key in obj:
            app.logger.debug("key is {} is it date {}".format(key, isinstance(getattr(model, key).type, Date)))
            if isinstance(getattr(model, key).type, DateTime):
                kwargs[key] = datetime.strptime(obj[key], date_format)
            else:
                kwargs[key] = obj[key]

            objs.append(kwargs)

    app.logger.debug("objs are {}".format(objs))

    db.session.bulk_update_mappings(model, objs)



class BaseView(FlaskView):
    model = None
    post_keys = []

    def index(self):
        return self.get(None)

    @try_except
    def get(self, id=None):
        if self.model is None:
            raise NotImplementedError("Define model")

        if id is not None:
            try:
                obj = db.session.query(self.model).filter_by(id=id).one().json
            except NoResultFound as x:
                raise UserError("No {} with id={}".format(model.__tablename__, id))

            return jsonify({"meta": {}, "data": obj})

        objs = [obj.json for obj in db.session.query(self.model).all()]

        return jsonify({"meta": {"len": len(objs)}, "data": objs}), 200

    @try_except
    def post(self):
        if self.model is None or not self.post_keys:
            raise NotImplementedError("Define model and post_keys")

        data = request.json['data']

        objs = bulk_save(self.model, data, self.post_keys)

        objs = [obj.json for obj in objs]

        db.session.commit()

        return jsonify({"meta": {"len": len(objs)}, "data": objs}), 200

    @try_except
    def delete(self):
        if self.model is None:
            raise NotImplementedError("Define model")

        delete_all = False

        form = request.json

        # TODO clean this up
        if 'meta' in form:
            if 'delete_all' in form['meta']:
                delete_all = form['meta']['delete_all']

        if delete_all:
            num_deleted = db.session.query(self.model).delete()
        else:
            data = request.json['data']
            ids = [obj['id'] for obj in data]
            num_deleted = 5
            num_deleted = db.session.query(self.model).filter(self.model.id.in_((id for id in ids))).delete(synchronize_session='fetch')

        db.session.commit()

        return jsonify({'meta': {'num_deleted': num_deleted}, 'data': {}}), 200

    @try_except
    def put(self):
        if self.model is None:
            raise NotImplementedError("Define model")

        # TODO need to handle date conversion dynamically
        # Should probably just read sqlalchemy documentation for once and learn to dynamically inspect columns easily

        data = request.json['data']
        if not isinstance(data, list):
            raise UserError({"data attribute should be dict/json"})

        bulk_update(self.model, data)

        db.session.commit()

        return jsonify({'meta': {}, 'data': {}}), 200




class CourseView(BaseView):
    model = Course
    post_keys = ['name']


class ClassView(BaseView):
    model = Class
    post_keys = ['start_dt', 'end_dt', 'course_id']

views = [CourseView, ClassView]
for view in views:
    view.register(app, route_prefix='/api/')
