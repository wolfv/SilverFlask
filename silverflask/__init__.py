#! ../env/bin/python

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from silverflask import assets
import os

from silverflask.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)

from silverflask.filestorage_backend import LocalFileStorageBackend
from silverflask.sqlalchemy import SQLAlchemy

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

    upload_path = os.path.join(app.instance_path, app.config["SILVERFLASK_UPLOAD_FOLDER"])
    app.config["SILVERFLASK_ABSOLUTE_UPLOAD_PATH"] = upload_path
    app.storage_backend = LocalFileStorageBackend(upload_path)
    app.config['ENV'] = env

    db.init_app(app)
    app.logger.debug("DB Initialized")

    # init the cache
    cache.init_app(app)

    debug_toolbar.init_app(app)

    # Setup user handling
    from silverflask.models import User

    user_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(user_adapter)
    user_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in list(assets_loader.load_bundles().items()):
        assets_env.register(name, bundle)

    # register our blueprints
    from silverflask.controllers.main import setup_processors, init_blueprint
    from silverflask.controllers.cms import bp as cms_bp

    setup_processors(app)
    main = init_blueprint(app)
    app.register_blueprint(main)
    app.register_blueprint(cms_bp, url_prefix='/admin')

    from silverflask.controllers.page_controller import Controller, SiteTreeController
    c = Controller()
    stc = SiteTreeController()
    app.register_blueprint(c.create_blueprint())
    app.register_blueprint(stc.create_blueprint())

    with app.app_context():
        db.create_all()

    # for rule in app.url_map.iter_rules():
    #     print(rule)
    return app