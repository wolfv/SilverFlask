class Config(object):
    SECRET_KEY = 'secret key'

    # Silver Flask
    SILVERFLASK_UPLOAD_FOLDER = "uploads/"

    # User
    USER_LOGIN_TEMPLATE = "user/login.html"
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    CACHE_TYPE = 'simple'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    ASSETS_DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    SQLALCHEMY_ECHO = False

    HOME_URLSEGMENT = 'home'

    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False
    LOGGER_NAME = "silverflask"


class TestConfig(DevConfig):
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
