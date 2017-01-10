# -*- coding: utf-8 -*-
from os import getenv
from requests_toolbelt.adapters import appengine; appengine.monkeypatch()
import urllib3; urllib3.disable_warnings()
from google.appengine.ext.appstats import recording

from flask import Flask

__all__ = ['create_app']


def create_app(config=None, **kwargs):
    app = Flask(__name__, **kwargs)
    _configure_app(app, config)
    _configure_blueprints(app)
    _configure_error_handlers(app)
    return recording.appstats_wsgi_middleware(app)


def _configure_app(app, config=None):
    app.secret_key = 'super secret string'
    app.debug = not getenv('SERVER_SOFTWARE', '').startswith('Google App Engine')


def _configure_blueprints(app):
    from bot import blueprint as bot_blueprint
    app.register_blueprint(bot_blueprint)


def _configure_error_handlers(app):
    @app.errorhandler(500)
    def application_error(error):
        return 'Unexpected error: {}'.format(error), 500
