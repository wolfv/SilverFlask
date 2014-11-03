from wtforms.fields import FileField, TextAreaField, Field
from wtforms.widgets.core import HTMLString, html_params
from flask import render_template
from silverflask import db

class AsyncFileUploadWidget(object):
    """
    Renders a file input chooser field.
    """
    def __init__(self, query=None, relation=None, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.relation = relation
        print(self.query)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        elem = None
        if field._value():
            elem = db.session.query(self.relation).get(field._value())

        return render_template("forms/AsyncFileUploadWidget.html",
                               value=field._value(),
                               elem=elem,
                               **kwargs)


class LivingDocsWidget(object):
    input_type = 'livingdocs'
    def __call__(self, field, **kwargs):
        print(kwargs)
        print(field._value())
        return render_template("forms/LivingDocsWidget.html",
                               field_name=field.id,
                               value=field._value(),
                               **kwargs)

class GridFieldWidget(object):

    def unpack_display_rows(self, display_rows):
        self.display_rows = []
        for d in display_rows:
            if isinstance(d, str):
                self.display_rows.append({"name": d})
            elif isinstance(d, dict):
                self.display_rows.append(d)
            else:
                raise TypeError("Display Row must be str or dict")

    def _generate_urls(self, **kwargs):
        def url():
            return "/admin/gridfield/{0}/{1}/{2}/{3}".format(
                self.record_classname,
                self.record_id,
                self.function_name,
                self.field_name
            )
        if not self.urls:
            self.urls = {
                "get": url(),
                "add": url() + "/add",
                "sort": url() + "/sort"
            }

    def __init__(self, query=None, display_rows=None, buttons=None,
                 function_name="get_cms_form", field_name=None,
                 record_id=None, record_classname=None, urls=None, **kwargs):
        # super().__init__(**kwargs)
        self.query = query
        self.buttons = buttons
        self.unpack_display_rows(display_rows)
        self.function_name = function_name
        self.field_name = field_name
        self.record_id = record_id
        self.record_classname = record_classname
        self.urls = urls
        self._generate_urls()

    def __call__(self, field, **kwargs):
        print(self.field_name)
        return render_template("forms/GridFieldWidget.html",
                               field_name=self.field_name,
                               buttons=self.buttons,
                               # entries=self.query(),
                               display_rows=self.display_rows,
                               urls=self.urls,
                               **kwargs)


class AsyncFileUploadField(FileField):
    def __init__(self, relation=None, **kwargs):
        super().__init__(**kwargs)
        self.relation = relation
        self.sqlrelation = db.relationship(relation)
        self.query = lambda: db.session.query(relation)
        self.widget = AsyncFileUploadWidget(
            relation=self.relation,
            query=self.query
        )
        # print(dir(self.sqlrelation))
        # print(self.sqlrelation.__dict__)

class LivingDocsField(TextAreaField):
    widget = LivingDocsWidget()


class GridField(Field):
    class AddButton():
        name = "Add Entry"

    record_id = None
    record_classname = None

    def __init__(self, parent_record=None, query=None, buttons=None,
                 urls=None, display_rows=None, field_name=None, **kwargs):
        super().__init__(**kwargs)
        if parent_record:
            self.record_id = parent_record.id
            self.record_classname = parent_record.__class__.__name__
        self.query = query
        self.buttons = buttons
        self.widget = GridFieldWidget(query=self.query,
                                      buttons=self.buttons,
                                      record_id=self.record_id,
                                      record_classname=self.record_classname,
                                      display_rows=display_rows,
                                      field_name=field_name,
                                      urls=urls,
                                      **kwargs)