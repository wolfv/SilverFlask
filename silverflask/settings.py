class Config(object):
    SECRET_KEY = 'secret key'
    USER_LOGIN_TEMPLATE = "user/login.html"

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

class TestConfig(DevConfig):
    print("THIS IS THE TESTCONFIGN")
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
