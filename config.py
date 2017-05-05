import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # For configuration that is common across all stages.
    SECRET_KEY='JKHDJFAHUIB483475890395#@#$JDFHHA'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI= 'postgresql://localhost/bucket'
    SECRET_KEY = 'p9Bv<3Eid9%$i01'


class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI= 'sqlite:////'+basedir+'/test.db'



app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
