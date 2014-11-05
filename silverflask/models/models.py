from flask.ext.login import UserMixin, AnonymousUserMixin
from silverflask.fields import LivingDocsField, AsyncFileUploadField, GridField
from wtforms.fields import HiddenField
from .SiteTree import SiteTree
from sqlalchemy.sql import func, select, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect
from .GalleryImage import  GalleryImage
from silverflask import db

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
        cms_form.content_json = HiddenField()
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

    images = db.relationship("GalleryImage")

    def get_cms_form(self):
        from .DataObject import OrderedForm
        from wtforms import fields
        form = OrderedForm()
        form.add_to_tab("Root.Main", fields.StringField(name="Text mich voll"))
        form.add_to_tab("Root.Main", fields.StringField(name="Nochsoeintext"))
        return form
        form = super().get_cms_form()
        button_list = []
        button_list.append(GridField.AddButton())
        form.images = GridField(
            parent_record=self,
            query=lambda: GalleryImage.query_factory().filter(GalleryImage.page_id == self.id),
            buttons=button_list,
            field_name="images",
            display_rows=["id", "caption", "sort_order"])
        return form