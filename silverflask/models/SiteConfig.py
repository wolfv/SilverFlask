from . import DataObject
from flask import current_app
from flask_wtf import Form
from wtforms import fields
from silverflask import db
from silverflask.models.OrderedForm import OrderedFormFactory

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

    @staticmethod
    def get_available_themes():
        return [(theme.identifier, theme.name) for theme in current_app.silverflask_theme_manager.themes.values()]

    def get_cms_form(cls):
        form = OrderedFormFactory()
        form.add_to_tab("Root.Main", fields.StringField(name='title'))
        form.add_to_tab("Root.Main", fields.StringField(name='tagline'))
        form.add_to_tab("Root.Main", fields.SelectField(name='theme', choices=cls.get_available_themes()))
        form.add_to_tab("Root.Buttons", fields.SubmitField("Save", name='Save'))
        return form

    @classmethod
    def get_current(cls):
        return cls.query.one()