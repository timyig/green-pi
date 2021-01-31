import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from db import db


def create_app():
    app = Flask(__name__)
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=log_level)
    app.config.from_object(os.getenv('APP_SETTINGS', 'config.Config'))
    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    from api import schedules_bp
    app.register_blueprint(schedules_bp)

    return app
