from . import DataObject
from flask_wtf import Form
from wtforms import fields
from silverflask import db


class SiteConfig(DataObject, db.Model):
    """
    class SiteConfig

    Holds global variables such as theme selection,
    site title or tagline.

    :ivar title: page title (shown in <title> tag)
    :ivar tagline: tagline of the website, can be used in the template
    :ivar theme: Not used now, could later hold the location of a template folder
    """
    __table_args__ = {'extend_existing': True}
    title = db.Column(db.String(250))
    tagline = db.Column(db.String(250))
    theme = db.Column(db.String(250))

    def get_cms_form(cls):
        form = type("SiteConfigForm", (Form, ), {})
        form.title = fields.StringField()
        form.tagline = fields.StringField()
        form.theme = fields.SelectField(choices=[("Test", "Test")])
        form.submit = fields.SubmitField("Save")
        return form