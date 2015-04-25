from silverflask.fields import LivingDocsField, AsyncFileUploadField, GridField
from wtforms.fields import HiddenField, StringField, SubmitField
from .SiteTree import SiteTree
from .GalleryImage import  GalleryImage
from silverflask import db
from .OrderedForm import OrderedFormFactory
from silverflask.models import ImageObject


class Page(SiteTree):
    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    content_json = db.Column(db.UnicodeText)

    template = "page.html"

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

    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    second_content = db.Column(db.UnicodeText)
    subtitle = db.Column(db.String)

    images = db.relationship("GalleryImage")

    header_image_id = db.Column(db.Integer, db.ForeignKey('imageobject.id'))
    header_image = db.relationship("ImageObject")

    template = "superpage.html"
    allowed_children = ["SuperPage"]
    icon = 'glyphicon glyphicon-flash'

    def get_cms_form(self):
        from wtforms import fields
        from silverflask.fields import AsyncFileUploadField
        # Setup Gridfield
        button_list = []
        button_list.append(GridField.AddButton())
        g = GridField(
            parent_record=self,
            query=lambda: GalleryImage.query.filter(GalleryImage.page_id == self.id),
            buttons=button_list,
            field_name="images",
            display_cols=[{"name": "id", "hidden": True}, "caption", {"name": "sort_order", "hidden": True}],
            name="images",
            sortable=True)

        form = OrderedFormFactory()
        form.add_to_tab("Root.Main", fields.StringField(name="name", default=1))
        form.add_to_tab("Root.Main", fields.TextAreaField(name="content"), before="asdasd")
        form.add_to_tab("Root.Main", AsyncFileUploadField(ImageObject, name="header_image_id"))
        form.add_to_tab("Root.Gallery", g)
        form.add_to_tab("Root.Buttons", SubmitField("Save", name="Submit"))
        form.add_to_tab("Root.Buttons", SubmitField("Publish", name="Publish"))

        return form
