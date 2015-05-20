#! ../env/bin/python

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.assets import Environment, Bundle

from silverflask import assets
import os

from silverflask.extensions import (
    cache,
    debug_toolbar,
    login_manager
)

from silverflask.filestorage_backend import LocalFileStorageBackend
from silverflask.sqlalchemy import SQLAlchemy

from flask.ext.migrate import Migrate
from flask_user import UserManager, SQLAlchemyAdapter

db = SQLAlchemy()

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    app.config['ENV'] = env

    return init_app(app)

def init_app(app):
    db.init_app(app)
    cache.init_app(app)
    debug_toolbar.init_app(app)
    app.template_folder = os.path.join(os.path.dirname(__file__), 'templates/')

    migrate = Migrate(app, db)

    # Import and register the different asset bundles
    assets_env = Environment(app)
    assets_env.load_path = [os.path.join(os.path.dirname(__file__), 'static')]
    assets_env.directory = os.path.join(os.path.dirname(__file__), 'static')
    assets_env.url = '/admin/static/'
    # assets_env.register('js_all', js)
    print("directory ", assets_env.directory, os.path.join(os.path.dirname(__file__), 'static/'))
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in list(assets_loader.load_bundles().items()):
        assets_env.register(name, bundle)

    # Setup user handling
    from silverflask.models import User

    user_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(user_adapter)
    user_manager.init_app(app)

    ###
    #  SILVERFLASK
    ###

    upload_path = os.path.join(app.instance_path, app.config["SILVERFLASK_UPLOAD_PATH"])
    app.config["SILVERFLASK_ABSOLUTE_UPLOAD_PATH"] = upload_path
    app.storage_backend = LocalFileStorageBackend(upload_path)


    from silverflask.controllers.page_controller import SiteTreeController
    app.register_blueprint(SiteTreeController.create_blueprint(app))

    from silverflask.core.dev_controller import DevController
    app.register_blueprint(DevController.create_blueprint(app))

    from silverflask.controllers.cms_controller import CMSController, PagesCMSController, FilesCMSController, \
        DataObjectCMSController

    app.register_blueprint(CMSController.create_blueprint(app))
    app.register_blueprint(DataObjectCMSController.create_blueprint(app))
    app.register_blueprint(PagesCMSController.create_blueprint(app))
    app.register_blueprint(FilesCMSController.create_blueprint(app))
    from silverflask.controllers.security_controller import SecurityController
    app.register_blueprint(SecurityController.create_blueprint(app))


    from silverflask.core.theme import init_themes
    init_themes(app)

    from silverflask.controllers.main import setup_processors, init_blueprint
    from silverflask.controllers.cms import bp as cms_bp

    setup_processors(app)
    main = init_blueprint(app)
    app.register_blueprint(main)
    app.register_blueprint(cms_bp, url_prefix='/admin')


    # for rule in app.url_map.iter_rules():
    #     print(rule)

    return app
