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


versioned_classes = ["sitetree"]
created_tables = []

def create_live_table(cls):

    tablename = cls.__tablename__ + "_live"
    if tablename in created_tables or cls.__tablename__ in created_tables:
        return
    created_tables.append(tablename)
    columns = []

    print("Creating Live table for: %s" % cls.__tablename__)

    ins = sainspect(cls)

    for c in cls.__table__.columns:
        if c.foreign_keys:
            # TODO Make this general
            columns.append(db.Column(c.key, db.Integer(),
                                     db.ForeignKey("sitetree_live.id"),
                                     primary_key=c.primary_key,
                                     default=c.default))
        else:
            columns.append(c.copy())

    cls.LiveTable = table = sa.schema.Table(
        tablename,
        cls.__table__.metadata,
        *columns
    )

    args = {}

    for key, value in cls.__dict__.items():
        if type(value) is types.FunctionType:
            args.update({key: value})

    args.update({
        "__table__": table
    })

    for column in columns:
        args[column.name] = column

    baseclass = tuple()
    for c in inspect.getmro(cls):
        if c != cls and c.__name__ == "SiteTree":
            print(c.__name__)
            baseclass = (c.LiveType, ) + baseclass
        elif c != cls and c.__name__ != "VersionedMixin":
            baseclass = (c, ) + baseclass

    # Reverse baseclass mro
    baseclass = baseclass[::-1]

    print("FINDING RELATIONSHIPS %s" % cls.__name__)
    backrefs = []
    rs = [r for r in ins.relationships]
    for r in rs:
        if r.parent == cls.__mapper__:
            print("There is a relation defined %s with Key: %r" % (cls.__name__, r))

            if r.target.fullname.endswith("version"):
                continue

            if r.key in backrefs:
                continue

            key = r.key
            target = ""
            if r.target.fullname in versioned_classes:
                target = r.mapper.entity.__name__ + "Live"
            else:
                primaryjoin = copy.copy(r.primaryjoin)
                primaryjoin.left = args[primaryjoin.left.key]
                args[key] = db.relationship(r.mapper, viewonly=True, primaryjoin=primaryjoin,
                                            foreign_keys=[primaryjoin.right])
                continue
            if hasattr(r, "backref") and r.backref:
                print(r.backref)
                backref_key = r.backref[0]
                backrefs.append(backref_key)
                backref = r.backref[1]
                print(backref["remote_side"].arg)
                remote_side = None
                if hasattr(backref["remote_side"].cls, "LiveType") or backref["remote_side"].cls == cls:
                    orig_arg = backref["remote_side"].arg
                    arg_v = orig_arg.split(".")
                    arg_v[0] = arg_v[0] + "Live"
                    remote_side = ".".join(arg_v)
                    print(remote_side)
                    args[key] = db.relationship(target, backref=db.backref(backref_key, remote_side=remote_side), cascade="none, ")
                else:
                    args[key] = db.relationship(target, cascade="none, ")
            else:
                args[key] = db.relationship(target, cascade="none, ")

    if args.get("__create_live__"):
        del args["__create_live__"]

    if args.get("before_insert"): del args["before_insert"]
    if args.get("before_update"): del args["before_update"]
    if args.get("__versioned__"): del args["__versioned__"]

    args["template"] = getattr(cls, "template") if hasattr(cls, "template") else ""

    # print(methods)
    cls.LiveType = type(
        '%sLive' % cls.__name__,
        baseclass,
        args
    )
    cls.LiveType.__create_live__ = False
    mapper_args = {}
    if hasattr(cls, "__mapper_args__"):
        mapper_args = cls.__mapper_args__

    for key, arg in mapper_args.items():
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
        new_object = False
        if not t_obj:
            t_obj = t()
            new_object = True

        ins = sainspect(self.__class__)

        for column in ins.columns:
            print("KEY: %s : %s" % (column.name, getattr(self, column.name)))
            setattr(t_obj, column.name, getattr(self, column.name))
        if new_object:
            db.session.add(t_obj)
        db.session._enable_transaction_accounting = False
        db.session.commit()
        db.session._enable_transaction_accounting = True

classes_to_create = []

@event.listens_for(mapper, "instrument_class")
def instrumented_class(mapper, cls):
    if cls is not None and hasattr(cls, "__create_live__") \
        and cls not in classes_to_create and not cls.__name__.endswith("Live"):
        classes_to_create.append(cls)

@event.listens_for(mapper, 'after_configured')
def after_configured():
    for cls in classes_to_create:
        live_table = create_live_table(cls)
        cls.live_table_instance = live_table
    classes_to_create.clear()


import sqlalchemy as sa
sa.orm.configure_mappers()