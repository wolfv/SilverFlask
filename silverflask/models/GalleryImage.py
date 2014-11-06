# Just a test

from .DataObject import DataObject
from .OrderableMixin import OrderableMixin
from . import FileObject, ImageObject

from silverflask import db
from wtforms import fields
from flask_wtf import Form
from silverflask.fields import AsyncFileUploadField

class GalleryImage(OrderableMixin, DataObject, db.Model):
    caption = db.Column(db.String(250))
    image_id = db.Column(db.ForeignKey(FileObject.id))
    image = db.relationship("FileObject")

    page_id = db.Column(db.ForeignKey("superpage.id"))
    page = db.relationship("SuperPage")

    @classmethod
    def get_cms_form(cls):
        form = Form
        form.caption = fields.StringField("Caption")
        form.image_id = AsyncFileUploadField(relation=ImageObject)
        form.page_id = fields.IntegerField()
        form.submit = fields.SubmitField("Submit")
        return form

    def __init__(self):
        self.init_order(GalleryImage)
