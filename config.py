import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # For configuration that is common across all stages.
    SECRET_KEY=os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    '''
    Development configuration.
    '''
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/bucket')
    SECRET_KEY = 'p9Bv<3Eid9%$i01'


class ProductionConfig(Config):
    '''
    Put production configuration here.
    '''
    DEBUG = False

class TestingConfig(Config):
    '''
    Put testing configuration here.
    '''
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI= 'sqlite:////'+basedir+'/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
