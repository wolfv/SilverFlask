from flask.ext.login import UserMixin, AnonymousUserMixin
from flask_user import UserMixin
from silverflask import db
from sqlalchemy.orm import synonym
from .. import app
from . import DataObject



class User(DataObject, UserMixin, db.Model):
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True)

    email = db.Column(db.String, unique=True)
    
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    
    confirmed_at = db.Column(db.DateTime)
    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='1') 

    roles = db.relationship('Role', secondary='user_roles',
                             backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password):
        self.username = username
        self.password = app.user_manager.hash_password(password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Role(DataObject, db.Model):
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
