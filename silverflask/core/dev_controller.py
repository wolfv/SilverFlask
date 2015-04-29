import datetime
from flask import Blueprint
from flask.ext.migrate import init as init_migrations
from flask.ext.migrate import init as revision, upgrade, migrate, _get_config
from alembic import command, context
from alembic.context import EnvironmentContext
from alembic.script import ScriptDirectory
from alembic.util import CommandError
# register dev route

from . import Controller

class DevController(Controller):

    url_prefix = '/dev'
    urls = {
        '/migrate': 'migrate',
        '/heads': 'heads',
        '': 'index'
    }

    @staticmethod
    def migrate():
        now_str = datetime.datetime.now().strftime('%d-%m-%y-%H:%M')
        try:
            init_migrations()
        except CommandError as e:
            # Already initiated .., all good!
            pass

        migrate(message='silverflask_%s' % now_str)
        upgrade()
        return 'We\'ve upgraded the ship'

    @staticmethod
    def heads():
        config = _get_config(None)
        script = ScriptDirectory.from_config(config)
        with EnvironmentContext(
                config,
                script
            ) as ctx:
            print(ctx.get_head_revisions())
            print(script.get_current_head())
            rev = script.get_current_head()
            mig = script.get_revision(rev)
            print(mig)
            with open(mig.path, 'r') as fp:
                return fp.read()

    @staticmethod
    def index():
        return 'You have reached the dev methods, now choose: heads, or migrate!'