from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager

# Setup flask Cache
cache = Cache()

debug_toolbar = DebugToolbarExtension()

login_manager = LoginManager()
login_manager.login_view = "main.login"

