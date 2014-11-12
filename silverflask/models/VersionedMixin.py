# Stolen from https://gist.github.com/dtheodor/55325741f04f7d64daa5
# by github.com/dtheodor

from sqlalchemy_continuum import get_versioning_manager, make_versioned, \
    versioning_manager, version_class, transaction_class
from sqlalchemy_continuum.utils import version_obj
from sqlalchemy_continuum.plugins import TransactionMetaPlugin
from silverflask import db
from sqlalchemy.orm import mapper
from sqlalchemy import event
from flask import request
import copy
import types
from sqlalchemy import inspect as  sainspect
import inspect
meta_plugin = TransactionMetaPlugin()

make_versioned(plugins=[meta_plugin])

def create_live_table(cls):

    tablename = cls.__tablename__ + "_live"
    columns = []
    print("Creating Live table for: %s" % cls.__tablename__)
    print(cls.__dict__)
    ins = sainspect(cls)

    for c in cls.__table__.columns:
        if c.foreign_keys:
            # print(c.__dict__)
            columns.append(db.Column(c.key, db.Integer(),
                                     db.ForeignKey("sitetree_live.id"),
                                     primary_key=c.primary_key,
                                     default=c.default))
        else:
            print(c.default)
            columns.append(c.copy())

    cls.LiveTable = table = sa.schema.Table(
        tablename,
        cls.__table__.metadata,
        *columns
    )

    args = {}

    # for r in ins.relationships:
    #     print(r.__dict__)


    for key, value in cls.__dict__.items():
        if type(value) is types.FunctionType:
            print("WOW a function %s", key)
            args.update({key: value})

    args.update({
        "__table__": table
    })

    for column in columns:
        args[column.name] = column

    baseclass = (db.Model, )
    for c in inspect.getmro(cls):
        if c != cls and c.__name__.lower() == "sitetree":
            baseclass = (c.LiveType, ) + baseclass
    if cls.__name__ == "SiteTree":
        args["children"] = db.relationship('%sLive' % cls.__name__,
                                       cascade="all",
                                       backref=db.backref("parent", remote_side='%sLive.id' % cls.__name__),
                                       )

    # print(methods)
    cls.LiveType = type(
        '%sLive' % cls.__name__,
        baseclass,
        args
    )

    mapper_args = {}
    if hasattr(cls, "__mapper_args__"):
        mapper_args = cls.__mapper_args__
    for key, arg in mapper_args.items():
        print(table.columns.__dict__)
        print(key, arg)
        if key == "polymorphic_on":
            # remap column!
            mapper_args[key] = table.columns[arg.name]
        elif key == "polymorphic_identity":
            mapper_args[key] = mapper_args[key] + "_live"

    live_mapper = mapper(cls, cls.LiveTable,
                         non_primary=True,
                         **mapper_args)
    cls.live_mapper = live_mapper
    return cls.LiveTable


class VersionedMixin(object):
    """Base class for SQL Alchemy continuum objects that supports tagging"""
    __versioned__ = {
        'base_classes': (db.Model, )
    }

    __create_live__ = True

    class __metaclass__(type):
        @property
        def query(cls):
            print(request.args)
            if request.args.get("draft"):
                return db.session.query(cls)
            return db.session.query(cls.LiveType)


    @classmethod
    def live_table(cls):
        return cls.__tablename__ + "_live"

    def get_published(self):
        return self

    def mark_as_published(self):
        print("Publishing Page %d \n\n" % self.id)
        live_table_name = self.live_table()

        t = self.LiveType
        t_obj = db.session.query(t).get(self.id)
        print(t_obj)


        if not t_obj:
            t_obj = t()
            db.session.add(t_obj)

        ins = sainspect(self.__class__)

        for column in ins.columns:
            print("KEY: %s : %s" % (column.name, getattr(self, column.name)))
            setattr(t_obj, column.name, getattr(self, column.name))
        db.session.commit()

classes_to_create = []

@event.listens_for(mapper, "instrument_class")
def instrumented_class(mapper, cls):
    if hasattr(cls, "__create_live__"):
        classes_to_create.append(cls)

@event.listens_for(mapper, 'after_configured')
def after_configured():
    for cls in classes_to_create:
        live_table = create_live_table(cls)
        cls.live_table_instance = live_table
    classes_to_create.clear()


import sqlalchemy as sa
sa.orm.configure_mappers()