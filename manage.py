#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from silverflask import create_app, db
from silverflask.models import User, Page

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('SILVERFLASK_ENV', 'dev')
app = create_app('silverflask.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """
    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    """
    Creates a database with the defined models
    and also adds the default records that are needed for the CMS:
    Admin User, Admin Role, Default first page, and stuff
    """

    db.create_all()
    from silverflask.models import User
    from silverflask.models.User import Role
    if not len(Role.query.all()):
        admin_role = Role("admin", "Admin has all privileges")
        db.session.add(admin_role)

    if not len(User.query.all()):
        # create standard user
        u = User("admin", "admin")
        u.firstname = "Default"
        u.lastname = "Admin"
        u.email = "admin"
        db.session.add(u)
        admin_role = Role.query.filter(Role.name == "admin").first()
        u.roles.append(admin_role)

    from silverflask.models import SiteConfig
    if not len(SiteConfig.query.all()):
        sc = SiteConfig()
        sc.title = "Your SilverFlask Website"
        sc.tagline = "This is a default installation"
        db.session.add(sc)

    if not len(Page.query.all()):
        page = Page()
        page.content = "<p>Please proceed to the admin interface at <a href='/admin'>admin</a>!</p>"
        page.name = "home"
        page.urlsegment = "home"
        db.session.add(page)
        page.mark_as_published()
    db.session.commit()


if __name__ == "__main__":
    manager.run()
