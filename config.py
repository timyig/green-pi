import os


class Config(object):
    """
    Base config class.
    """
    DEBUG = False
    TESTING = False
    CORS_AUTOMATIC_OPTIONS = True
    SECRET_KEY = 'fd8d782c2633851ce9be7329d3d6d126c1827450fdcc4eba5247e172f4d5f7f8ce1d0d353ed20890f19a7d6f28a46255'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('GREEN_PI_DB_CONNECTION', 'sqlite:///:memory:')


class TestingConfig(Config):
    """
    testing config.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('GREEN_PI_TEST_DB_CONNECTION',
        'postgresql://green-pi:green-pi@db:5432/green-pi-db-test')
