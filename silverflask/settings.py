import os
class Config(object):
    SECRET_KEY = 'secret key'

    # Silver Flask
    SILVERFLASK_UPLOAD_PATH = "uploads/"
    SILVERFLASK_THEME_PATH = "themes/"
    SILVERFLASK_HOME_URLSEGMENT = 'home'

    # User
    USER_LOGIN_TEMPLATE = "user/login.html"
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True

class ProdConfig(Config):
    sqlite_db_path = os.path.abspath('./database.db')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_db_path
    CACHE_TYPE = 'simple'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ASSETS_DEBUG = True
    sqlite_db_path = os.path.abspath('./database.db')
    print(sqlite_db_path)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_db_path
    SQLALCHEMY_ECHO = False


    CACHE_TYPE = 'null'

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False
    LOGGER_NAME = "silverflask"


class TestConfig(DevConfig):
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # SQLALCHEMY_ECHO = True
