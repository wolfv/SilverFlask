from flask import render_template
from sqlalchemy.ext.declarative import declared_attr
from wtforms import fields
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import event


db = SQLAlchemy()

class OrderedFieldList():
    class TabNode():
        name = ""
        children = []
        tabs = []
        def __init__(self, name):
            self.name = name

        def get_tab(self, tabname):
            for c in self.tabs:
                if c.name == tabname:
                    return c
            return None

        def find(self, name):
            idx = 0
            for idx, child in enumerate(self.children):
                if child.name == name:
                    return idx
            return len(self.children)

    def __init__(self):
        self.root = self.TabNode("Root")

    def add_to_tab(self, tabname, field, before=None):
        location = tabname.split('.')
        prev_node = self.root
        if location[0] == "Root":
            del location[0]
        else:
            raise UserWarning("Error: Root must be in location")
        for l in location:
            node = prev_node.get_tab(l)
            if not node:
                node = self.TabNode(l)
                prev_node.tabs.append(node)
            prev_node = node

        index = node.find(before)
        node.children.insert(index, field)


class OrderedForm(Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fields = OrderedFieldList()

    def add_to_tab(self, tabname, field, before=None):
        return self._fields.add_to_tab(tabname, field, before)


class DataObject(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer(), primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    last_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    has_one = {}
    has_many = {}
    many_many = {}
    belongs_many_many = {}

    default_order = ""

    __mapper_args__ = {'always_refresh': True}

    database = ["id", "created_on", "last_modified"]

    # class CMSForm(Form):
    # name = fields.StringField("asdsadsa")
    #     submit = fields.SubmitField("Submit")

    def __new__(cls, *args, **kwargs):
        def before_insert_listener(mapper, connection, target):
            if hasattr(target, "before_insert"):
                target.before_insert(mapper, connection, target)

        def before_update_listener(mapper, connection, target):
            if hasattr(target, "before_update"):
                target.before_update(mapper, connection, target)

        event.listen(cls, 'before_insert', before_insert_listener)
        event.listen(cls, 'before_update', before_update_listener)

        return super().__new__(cls, *args, **kwargs)


    @classmethod
    def query_factory(cls):
        return db.session.query(cls).order_by(cls.last_modified.desc())

    @classmethod
    def get_cms_form(cls):
        if hasattr(cls, "CMSForm"):
            return cls.CMSForm
        FormClass = model_form(cls, db.session, base_class=Form)
        FormClass.submit = fields.SubmitField()
        del FormClass.last_modified
        del FormClass.created_on
        return FormClass

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
