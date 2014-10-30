from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect
from silverflask.fields import LivingDocsField, AsyncFileUpload
from wtforms import fields
from .SiteTree import SiteTree
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

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

class GridField(fields.Field):
    def __call__(self, *args, **kwargs):
        return render_template("gridfield.html")


class Page(SiteTree):
    __tablename__ = 'page'

    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    content_json = db.Column(db.UnicodeText)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    def get_cms_form(self):
        cms_form = super().get_cms_form()
        cms_form.content = LivingDocsField()
        return cms_form

class SuperPage(SiteTree):
    __tablename__ = 'superpage'

    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    second_content = db.Column(db.UnicodeText)
    subtitle = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }


