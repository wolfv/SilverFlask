#! ../env/bin/python
import os

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from silverflask import assets

from silverflask.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app.config.from_object(object_name)

    app.config['ENV'] = env

    #init the cache
    cache.init_app(app)

    debug_toolbar.init_app(app)

    #init SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in list(assets_loader.load_bundles().items()):
        assets_env.register(name, bundle)

    # register our blueprints
    from silverflask.controllers.main import main
    from silverflask.controllers.cms import bp as cms_bp
    app.register_blueprint(main)
    app.register_blueprint(cms_bp, url_prefix='/admin')
    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    create_app('appname.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
