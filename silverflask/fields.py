from wtforms.fields import FileField, TextAreaField, Field
from wtforms.widgets.core import HTMLString, html_params
from flask import render_template
from silverflask import db

import urllib.parse

class AsyncFileUploadWidget(object):
    """
    Renders a file input chooser field.
    """
    def __init__(self, query=None, relation=None, multiple=False, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.relation = relation
        self.multiple = multiple
        print(self.query)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        elem = None

        if field._value():
            elem = db.session.query(self.relation).get(field._value())

        return render_template("forms/AsyncFileUploadWidget.html",
                               value=field._value(),
                               elem=elem,
                               multiple=self.multiple,
                               **kwargs)


class LivingDocsWidget(object):
    input_type = 'livingdocs'
    def __call__(self, field, **kwargs):
        return render_template("forms/LivingDocsWidget.html",
                               field_name=field.id,
                               value=field._value(),
                               **kwargs)

class GridFieldWidget(object):

    def unpack_display_cols(self, display_cols):
        self.display_cols = []
        for d in display_cols:
            if isinstance(d, str):
                self.display_cols.append({"name": d})
            elif isinstance(d, dict):
                self.display_cols.append(d)
            else:
                raise TypeError("Display Col must be str or dict")

    def generate_urls(self, form_name, field_name):
        current_url = urllib.parse.urlparse(request.url)
        params = urllib.parse.parse_qs(request.url)
        def url(action):
            params.update({
                'form': form_name,
                'field': field_name,
                'action': action
            })
            # current_url.params = urllib.parse.urlencode(params)

            return request.url + '?' + urllib.parse.urlencode(params)
            # return request.url + "?form={}&field={}&action={}".format(
            #     form_name,
            #     field_name,
            #     action,
            # )
        print("Generating URL")
        if not self.urls:
            self.urls = {
                "get": url('get_entries'),
                "add": url('add_entry'),
                "sort": url('sort')
            }


    def __init__(self, query=None, display_cols=None, buttons=None,
                 function_name="get_cms_form", field_name=None,
                 record_id=None, record_classname=None, urls=None, sortable=False, **kwargs):
        # super().__init__(**kwargs)
        self.query = query
        self.buttons = buttons
        self.unpack_display_cols(display_cols)
        self.function_name = function_name
        self.field_name = field_name
        self.record_id = record_id
        self.record_classname = record_classname
        self.urls = urls
        self.sortable = sortable
        # self._generate_urls()

    def __call__(self, field, **kwargs):
        print(self.field_name)
        return render_template("forms/GridFieldWidget.html",
                               field_name=self.field_name,
                               buttons=self.buttons,
                               # entries=self.query(),
                               display_cols=self.display_cols,
                               urls=self.urls,
                               sortable=self.sortable,
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

from flask import jsonify, request, redirect, url_for
import types

class GridFieldController():
    def __init__(self, gridfield, form):
        self.gridfield = gridfield
        self.form = form
        self.controlled_class = self.gridfield.controlled_class

    def get_entries(self):
        if issubclass(self.gridfield.query.__class__, types.FunctionType):
            data = [r.as_dict() for r in self.gridfield.query()]
        else:
            data = [r.as_dict() for r in self.gridfield.query]
        for d in data:
            d["edit_url"] = url_for('DataObjectCMSController.edit', cls=self.gridfield.controlled_class.__name__, id_=d.id)
            d["DT_RowId"] = str(d["id"])
        return jsonify(data=data)

    def add_entry(self):
        cls = self.gridfield.controlled_class
        return redirect(url_for('DataObjectCMSController.add', cls=cls.__name__, relation_id=self.gridfield.record_id))
        elem = cls()
        elem.page_id = self.gridfield.record_id
        element_form = elem.get_cms_form()
        element_form_instance = element_form(request.form, obj=elem)
        if element_form_instance.validate_on_submit():
            element_form_instance.populate_obj(elem)
            db.session.add(elem)
            db.session.commit()
            return "elem " + str(elem.__dict__)

        return render_template("page/edit.html",
                               page_form=element_form_instance)

class GridField(Field):
    class AddButton():
        name = "Add Entry"

    record_id = None
    record_classname = None

    controller_class = GridFieldController

    def __init__(self, controlled_class=None, parent_record=None, query=None, buttons=None,
                 urls=None, display_cols=None, field_name=None, sortable=False, **kwargs):
        super().__init__(**kwargs)
        if parent_record:
            self.record_id = parent_record.id
            self.record_classname = parent_record.__class__.__name__
        self.controlled_class = controlled_class
        self.query = query
        self.buttons = buttons
        self.widget = GridFieldWidget(query=self.query,
                                      buttons=self.buttons,
                                      record_id=self.record_id,
                                      record_classname=self.record_classname,
                                      display_cols=display_cols,
                                      field_name=field_name,
                                      sortable=sortable,
                                      urls=urls,
                                      **kwargs)

