from flask import render_template
from sqlalchemy.ext.declarative import declared_attr
from wtforms import fields
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import event


db = SQLAlchemy()

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

        return super().__new__(cls)


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
