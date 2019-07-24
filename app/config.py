import os


class Flask_Config():
    """
        Конфигурационный класс приложения Flask
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT') or '/'
    if os.environ.get('DEVELOPMENT'):
        HOST = '0.0.0.0'
        PORT = '5000'
        DEBUG = True
        ENV = 'development'
        USE_RELOADER = True

    else:
        HOST = '127.0.0.1'
        PORT = '5000'
        DEBUG = False
        ENV = 'production'
