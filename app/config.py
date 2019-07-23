import os


class Flask_Config():
    """
        Конфигурационный класс приложения Flask
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT') or '/'
    HOST = '0.0.0.0'
    PORT = '5000'
    if os.environ.get('PRODUCTION'):
        DEBUG = False
        ENV = 'production'

    else:
        DEBUG = True
        ENV = 'development'
        USE_RELOADER = True
