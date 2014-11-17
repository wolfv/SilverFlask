from flask.ext.login import UserMixin, AnonymousUserMixin
from silverflask.fields import LivingDocsField, AsyncFileUploadField, GridField
from wtforms.fields import HiddenField, StringField, SubmitField
from .SiteTree import SiteTree
from sqlalchemy.sql import func, select, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect
from .GalleryImage import  GalleryImage
from silverflask import db
from .OrderedForm import OrderedForm
from . import User


class Page(SiteTree):
    __tablename__ = 'page'
    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    content_json = db.Column(db.UnicodeText)
    template = "page.html"
    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

    def get_cms_form(self):
        form = type("CMSOrderedForm", (OrderedForm, ), {})
        form.add_to_tab("Root.Main", StringField(name="name"))
        form.add_to_tab("Root.Main", LivingDocsField(name="content"))
        form.add_to_tab("Root.Main", HiddenField(name="content_json"))
        form.add_to_tab("Root.Settings", StringField(name="urlsegment"))
        form.add_to_tab("Root.Buttons", SubmitField("Save", name="Submit"))
        form.add_to_tab("Root.Buttons", SubmitField("Save & Publish", name="Publish"))

        return form


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

    template = "superpage.html"

    def get_cms_form(self):
        from wtforms import fields
        # Setup Gridfield
        button_list = []
        button_list.append(GridField.AddButton())
        g = GridField(
            parent_record=self,
            query=lambda: GalleryImage.query_factory().filter(GalleryImage.page_id == self.id),
            buttons=button_list,
            field_name="images",
            display_rows=["id", "caption", "sort_order"],
            name="images")

        form = type("CMSOrderedForm", (OrderedForm, ), {})
        form.add_to_tab("Root.Main", fields.StringField(name="name", default=1))
        form.add_to_tab("Root.Main", fields.TextAreaField(name="content"), before="asdasd")
        form.add_to_tab("Root.Gallery", g)
        form.add_to_tab("Root.Buttons", SubmitField("Save", name="Submit"))
        form.add_to_tab("Root.Buttons", SubmitField("Publish", name="Publish"))

        return form
