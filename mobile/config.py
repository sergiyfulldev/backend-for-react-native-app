import os


class BaseConfig(object):
    """
    Base Configuration for Flask. Applies to all applications using
    :class:`mobile.factory.configure_app()`
    """

    SECRET_KEY = 'ap!8$^o2idjt8&n!!'

    ENV = None

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    INSTANCE_FOLDER_PATH = os.path.join(os.path.expanduser("~"), 'Projects/Python/mobile-app-backend/')

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')

    DEBUG = False
    TESTING = False

    # Flask-Cache Settings
    CACHE_TYPE = 'memcached'  # Can be "memcached", "redis", etc.

    # Flask Debug-Toolbar Settings
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_NAME = 'application.db'
    DATABASE_PATH = os.path.join(INSTANCE_FOLDER_PATH, DATABASE_NAME)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH) # todo postgres

    POSTGRES_USER = "dddmaster"
    POSTGRES_PASSWORD = "12dbm4509"
    POSTGRES_HOST = "mobileappdb.czin67lju8j2.us-east-1.rds.amazonaws.com"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "mobileappdb"

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(user=POSTGRES_USER,password=POSTGRES_PASSWORD,host=POSTGRES_HOST,port=POSTGRES_PORT,db=POSTGRES_DB)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH)

    #todo fill credentials.

    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'f7f6fdd6fffce6'
    MAIL_PASSWORD = '3c280060595ba1'
    MAIL_DEFAULT_SENDER = 'noreply@whatever.com'


class DefaultConfig(BaseConfig):
    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class ProductionConfig(BaseConfig):
    """
    Configuration object from :class:`mobile.config.BaseConfig` for
    production Flask apps. Applies to all applications using
    :method:`mobile.factory.configure_app()`
    """

    ENV = 'prod'

    LOGLEVEL = 'INFO'

    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = 'mysql://'

    API_URL = ""


class TestConfig(BaseConfig):
    """
    Configuration object from :class:`mobile.config.BaseConfig`
    Configuration for Flask. Applies to all applications using
    :method:`mobile.factory.configure_app()`
    """
    SECRET_KEY = 'ap!8$^o2idjt8&n!!'

    LOGLEVEL = "DEBUG"

    DEBUG = True
    TESTING = True

    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'

    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class DevConfig(BaseConfig):
    ENV = "dev"
    SECRET_KEY = 'dev-12461'

    LOGLEVEL = "DEBUG"

    DEBUG = True
    TESTING = False

    INSTANCE_FOLDER_PATH = BaseConfig.PROJECT_ROOT
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')

    ASSETS_DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    CACHE_TYPE = 'memcached'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_NAME = 'development.db'
    DATABASE_PATH = os.path.join(BaseConfig.PROJECT_ROOT, DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DATABASE_PATH)