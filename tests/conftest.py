import os
import pytest

from sqlalchemy import text

from app import create_app
from db import db as _db


@pytest.fixture(scope='session')
def app(request):
    """
    :param Request request:
    :return Flask:
    """
    os.environ['APP_SETTINGS'] = 'config.TestingConfig'
    app = create_app()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def db(app, request):
    """
    A fixture to create a test DB for our session and destroy it after
    running the tests
    :param Flask app:
    :param Request request:
    :return SQLAlchemy:
    """
    def teardown():
        _db.session.remove()
        _db.drop_all()

    _db.app = app
    _db.create_all()

    """
    The following will execute an SQL file to insert some fixture data in the database
    to make the tests ready. I don't really like this way of populating data.
    I think it's better to insert fixture data programmatically which is described 
    in yaml / json files.
    """
    with open(os.path.join(app.root_path, 'tests/fixtures/test_data.sql')) as f:
        engine = _db.create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'), {})
        connection = engine.connect()
        connection.execute(text(f.read()))
        connection.close()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
