__author__ = 'mmoisen'

from . import app


from opbeat.contrib.flask import Opbeat

opbeat = Opbeat(
    app,
    organization_id='f9912cfead99443481626ec8571446dc',
    app_id='bf410a53b2',
    secret_token='f76c0fc391048436e4bfc5dd8d7df07835adfe25',
)