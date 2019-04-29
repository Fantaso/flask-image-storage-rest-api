from mongoengine import register_connection
import os


##########################################################
##########   FLASK SETTINGS                     ##########
class Development(object):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class Production(object):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False


class Testing(object):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True


APP_CONFIG = {
    'development': Development,
    'production': Production,
    'testing': Testing,
}


##########################################################
##########   MONGO DB AND MONGOENGINE SETTINGS  ##########
MONGODB_HOST = {
    'development': os.environ.get('MONGODB_HOST'),
    'production': os.environ.get('MONGODB_HOST'),
    'testing': os.environ.get('MONGODB_HOST'),
}


def db_connect(app_env):
    if app_env == 'development':
        return register_connection(alias='main', host=MONGODB_HOST.get('development'))
    elif app_env == 'production':
        return register_connection(alias='main', host=MONGODB_HOST.get('production'))
    elif app_env == 'testing':
        return register_connection(alias='main', host=MONGODB_HOST.get('testing'))
