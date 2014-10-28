from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect

from wtforms import fields

from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

db = SQLAlchemy()

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

class GridField(fields.Field):
    def __call__(self, *args, **kwargs):
        return render_template("gridfield.html")


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
    __mapper_args__ = {'always_refresh': True}
    database = ["id", "created_on", "last_modified"]

    # class CMSForm(Form):
    #     name = fields.StringField("asdsadsa")
    #     submit = fields.SubmitField("Submit")

    def get_cms_form(self):
        if hasattr(self, "CMSForm"):
            return self.CMSForm
        FormClass = model_form(self.__class__, db.session, base_class=Form)
        FormClass.submit = fields.SubmitField()
        del FormClass.children
        del FormClass.parent
        del FormClass.last_modified
        del FormClass.created_on
        # FormClass.gridfield = GridField()
        return FormClass
        return render_template("cms.html", form=FormClass(obj=self))
        return FormClass

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SiteTree(DataObject, db.Model):
    __tablename__ = "sitetree"
    parent_id = db.Column(db.Integer, db.ForeignKey('sitetree.id'))
    name = db.Column(db.String)
    database = ["parent_id", "name"]
    type = db.Column(db.String(50))
    urlsegment = db.Column(db.String(250))
    sort = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'sitetree',
        'polymorphic_on': type
    }

    children = db.relationship('SiteTree',
                            cascade="all",

                            # many to one + adjacency list - remote_side
                            # is required to reference the 'remote'
                            # column in the join condition.
                            backref=db.backref("parent", remote_side='SiteTree.id'),
    )

    def get_siblings(self):
        return SiteTree.query.filter(SiteTree.parent_id == self.parent_id)

    @staticmethod
    def get_sitetree():
        base_page = SiteTree.query.filter(SiteTree.parent_id == None)
        dest_list = []
        for p in base_page:
            dest_dict = {}
            print(p.name)
            SiteTree.recursive_build_tree(p, dest_dict)
            dest_list.append(dest_dict)
        return dest_list

    @staticmethod
    def recursive_build_tree(root_node, dest_dict):
        dest_dict.update(root_node.to_dict())
        children = root_node.children
        if children:
            dest_dict['children'] = []
            for child in children:
                temp_dict = {}
                dest_dict['children'].append(temp_dict)
                SiteTree.recursive_build_tree(child, temp_dict)
        else:
            return

    def to_dict(self):
        return {
            "text": self.name,
            "parent_id": self.parent_id,
            "created_on": self.created_on,
            "li_attr": {
                "data-pageid": str(self.id)
            },
            "a_attr": {
                "href": "/admin/edit/page/{0}".format(self.id)
            }
        }
    def append_child(self, child):
        self.children.append(child)

    def set_parent(self, parent_id):
        self.parent_id = parent_id

    def __init__(self):
        self.database.extend(super(SiteTree, self).database)

class Page(SiteTree):
    __tablename__ = 'page'

    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
    }

class SuperPage(SiteTree):
    __tablename__ = 'superpage'

    id = db.Column(db.Integer, db.ForeignKey('sitetree.id'), primary_key=True)
    content = db.Column(db.UnicodeText)
    second_content = db.Column(db.UnicodeText)
    subtitle = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }


class FileObject(DataObject, db.Model):
    location = db.Column(db.String(250))
    name = db.Column(db.String(250))

    def __init__(self, location):
        import os
        self.location = location
        self.name = os.path.splitext(location)[0]

    def url(self):
        return self.location

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }