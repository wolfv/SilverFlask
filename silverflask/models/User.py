from flask.ext.login import AnonymousUserMixin
from flask import current_app
from flask_user import UserMixin
from silverflask import db
from . import DataObject
from wtforms import fields, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

class UserRoles(db.Model):
    __tablename__ = "user_role"
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)

class User(DataObject, UserMixin, db.Model):
    """
    The base User model.
    """
    username = db.Column(db.String, unique=True)

    firstname = db.Column(db.String)
    lastname = db.Column(db.String)

    email = db.Column(db.String, unique=True)

    password = db.Column(db.String)

    confirmed_at = db.Column(db.DateTime)
    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='1') 

    roles = db.relationship('Role', secondary=UserRoles.__tablename__,
                             backref=db.backref('users', lazy='dynamic'))

    auto_form_exclude = DataObject.auto_form_exclude + ['confirmed_at', 'is_enabled']

    def __init__(self, username, password, email=None, is_enabled=True):
        self.username = username
        self.password = current_app.user_manager.hash_password(password)
        self.email = email
        self.is_enabled = is_enabled

    @property
    def name(self):
        return str(self.firstname) + " " + str(self.lastname)

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

    def set_password(self, new_password):
        self.password = current_app.user_manager.hash_password(new_password)

    def as_dict(self):
        d = super().as_dict()
        if d["password"]:
            del d["password"]
        d.update({"name": self.name})
        return d

    @classmethod
    def get_cms_form(cls):
        form = super().get_cms_form()
        roles = [(r.id, r.name) for r in db.session.query(Role).all()]
        form.add_to_tab("Root.Main", fields.PasswordField("New Password",
                                                          [validators.EqualTo('new_password_confirmation',
                                                                              message='Passwords must match')],
                                                          name='new_password'))
        form.add_to_tab("Root.Main", fields.PasswordField("Repeat New Password", name='new_password_confirmation'))
        form.add_to_tab("Root.Main", QuerySelectMultipleField('Role', query_factory=lambda: Role.query,
                                                              get_label=lambda x: x.name,
                                                              get_pk=lambda x: x.id,
                                                              name='roles'))
        del form.fields["password"]
        return form


class Role(DataObject, db.Model):
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description


