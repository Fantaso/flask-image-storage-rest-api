from mongoengine import register_connection


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
    'development': 'mongodb+srv://fantaso:cmmaran1986@cluster0-rjehl.mongodb.net/test?retryWrites=true',
    'production': 'mongodb+srv://fantaso:cmmaran1986@cluster0-rjehl.mongodb.net/test?retryWrites=true',
    'testing': 'mongodb+srv://fantaso:cmmaran1986@cluster0-rjehl.mongodb.net/test?retryWrites=true',
}


def db_connect(app_env):
    if app_env == 'development':
        return register_connection(alias='main', host=MONGODB_HOST.get('development'))
    elif app_env == 'production':
        return register_connection(alias='main', host=MONGODB_HOST.get('production'))
    elif app_env == 'testing':
        return register_connection(alias='main', host=MONGODB_HOST.get('testing'))
