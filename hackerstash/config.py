class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'teapot'
    SQLALCHEMY_DATABASE_URI = 'postgresql://hackerstash:hackerstash@db/hackerstash'


class TestingConfig(Config):
    TESTING = True
