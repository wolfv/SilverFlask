from silverflask.fields import LivingDocsField, AsyncFileUploadField, GridField
from wtforms.fields import HiddenField, StringField, SubmitField
from .SiteTree import SiteTree
from .GalleryImage import  GalleryImage
from silverflask import db as alchemy
from .OrderedForm import OrderedFormFactory
from silverflask.models import ImageObject
from sqlalchemy.event import listen
from sqlalchemy import event


class Page(SiteTree):

    # id = alchemy.Column(alchemy.Integer(), alchemy.ForeignKey("sitetree.id"), primary_key=True)
    # content = alchemy.Column(alchemy.UnicodeText)
    # content_json = alchemy.Column(alchemy.UnicodeText)

    template = "page.html"

    # Potential future way of creating models
    db = {
        "id": {
          'type': 'Integer',
          'foreign_key': 'sitetree.id',
          'primary_key': True
        },
        "content": "UnicodeText",
        "content_json": "UnicodeText"
    }

    def get_cms_form(self):
        form = OrderedFormFactory()
        form.add_to_tab("Root.Main", StringField(name="name"))
        form.add_to_tab("Root.Main", LivingDocsField(name="content"))
        form.add_to_tab("Root.Main", HiddenField(name="content_json"))
        form.add_to_tab("Root.Settings", StringField(name="urlsegment"))
        form.add_to_tab("Root.Buttons", SubmitField("Save", name="Submit"))
        form.add_to_tab("Root.Buttons", SubmitField("Save & Publish", name="Publish"))
        return form


class SuperPage(SiteTree):

    db = {
        'second_content': 'UnicodeText'
    }

    __abstract_inherit__ = [Page]
    # id = alchemy.Column(alchemy.Integer(), alchemy.ForeignKey("sitetree.id"), primary_key=True)

    # content = alchemy.Column(alchemy.UnicodeText)
    second_content = alchemy.Column(alchemy.UnicodeText)
    subtitle = alchemy.Column(alchemy.String)

    has_one = {
        'header_image': 'ImageObject'
    }

    has_many = {
        'images': 'GalleryImage'
    }

    many_many = {
        'sample_images': 'GalleryImage'
    }
    # header_image_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('imageobject.id'))
    # header_image = alchemy.relationship("ImageObject")

    # template = "superpage.html"
    allowed_children = ["SuperPage"]
    icon = 'glyphicon glyphicon-flash'

    # def get_cms_form(self):
    #     from wtforms import fields
    #     from silverflask.fields import AsyncFileUploadField
    #     # Setup Gridfield
    #     button_list = []
    #     button_list.append(GridField.AddButton())
    #     g = GridField(
    #         parent_record=self,
    #         query=lambda: GalleryImage.query.filter(GalleryImage.page_id == self.id),
    #         buttons=button_list,
    #         field_name="images",
    #         display_cols=[{"name": "id", "hidden": True}, "caption", {"name": "sort_order", "hidden": True}],
    #         name="images",
    #         sortable=True)
    #
    #     form = OrderedFormFactory()
    #     form.add_to_tab("Root.Main", fields.StringField(name="name", default=1))
    #     form.add_to_tab("Root.Main", fields.TextAreaField(name="content"), before="asdasd")
    #     form.add_to_tab("Root.Main", AsyncFileUploadField(ImageObject, name="header_image_id"))
    #     form.add_to_tab("Root.Gallery", g)
    #     form.add_to_tab("Root.Buttons", SubmitField("Save", name="Submit"))
    #     form.add_to_tab("Root.Buttons", SubmitField("Publish", name="Publish"))
    #
    #     return form


class ErrorPage(SiteTree):
    id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('sitetree.id'), primary_key=True)

    content = alchemy.Column(alchemy.UnicodeText)
    content_json = alchemy.Column(alchemy.UnicodeText)
    error_code = alchemy.Column(alchemy.Integer, nullable=False)


class FantasticPage(SiteTree):
    __abstract_inherit__ = [Page]
    db = {
        'test': 'Boolean',
        'anzeige': 'Text',
        'votes': 'Integer'
    }


class CrazyPage(SiteTree):
    __abstract_inherit__ = [Page]
    db = {
        'reddit_id': 'Integer'
    }