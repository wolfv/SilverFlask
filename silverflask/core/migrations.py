import datetime
from flask import Blueprint
from flask.ext.migrate import init as init_migrations
from flask.ext.migrate import init as revision, upgrade, migrate, _get_config
from alembic import command, context
from alembic.context import EnvironmentContext
from alembic.script import ScriptDirectory
from alembic.util import CommandError
# register dev route
bp = Blueprint('dev', __name__)

@bp.route('/dev/migrate')
def do_migration():
    now_str = datetime.datetime.now().strftime('%d-%m-%y-%H:%M')
    try:
        init_migrations()
    except CommandError as e:
        pass
    migrate(message="silverflask_%s" % now_str)
    upgrade()
    return "We've upgraded the ship"

@bp.route('/dev/heads')
def get_heads():
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
        print(dir(mig))
        print(mig.read())
    command.heads(config, verbose=True,
                  resolve_dependencies=True)