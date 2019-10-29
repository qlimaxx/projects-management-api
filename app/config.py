class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = '1nlGIl5nNlRKiat3QtK7'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    DEBUG = False
    TESTING = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db.test/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
