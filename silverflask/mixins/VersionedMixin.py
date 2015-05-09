# Stolen from https://gist.github.com/dtheodor/55325741f04f7d64daa5
# by github.com/dtheodor

from sqlalchemy_continuum import get_versioning_manager, make_versioned, \
    versioning_manager, version_class, transaction_class
from sqlalchemy_continuum.utils import version_obj
from sqlalchemy_continuum.plugins import TransactionMetaPlugin
from sqlalchemy.orm import mapper
from sqlalchemy.orm.interfaces import *
from sqlalchemy import event
from flask import current_app, app
import copy
import types
from sqlalchemy import inspect as sainspect
import inspect

import logging
logger = logging.getLogger('VersionedLogger')
logger.setLevel(logging.DEBUG)


from silverflask import db
from silverflask.helper import classproperty

meta_plugin = TransactionMetaPlugin()

make_versioned(plugins=[meta_plugin])

versioned_classes = []
versioned_tables = []
created_tables = []

def create_live_table(cls):
    tablename = cls.__tablename__ + "_live"
    if tablename in created_tables or cls.__tablename__ in created_tables:
        return
    created_tables.append(tablename)
    columns = []
    logger.debug("Creating Live table for: %s" % cls.__tablename__)

    ins = sainspect(cls)

    versioned_basetable = tablename
    baseclass = tuple()
    for c in inspect.getmro(cls):
        if c != cls and c.__name__ in versioned_classes:
            versioned_basetable = c.__table__.name + "_live"
            baseclass = (c.LiveType, ) + baseclass
        elif c != cls and c.__name__ != "VersionedMixin":
            baseclass = (c, ) + baseclass

    # Reverse baseclass mro
    baseclass = baseclass[::-1]

    for c in cls.__table__.columns:
        # What is happening
        # TODO: Check if this also works with different relationships...
        new_keys = []
        if c.foreign_keys:
            for k in c.foreign_keys:
                key_target = k.column.table.name
                if key_target in versioned_tables:
                    new_keys.append(db.ForeignKey(key_target + "_live." + k.column.key))
                else:
                    new_keys.append(db.ForeignKey(k.target_fullname))

            columns.append(db.Column(c.key, db.Integer(),
                                     new_keys[0],
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

    backrefs = []
    rs = [r for r in ins.relationships]
    for r in rs:
        if r.parent == cls.__mapper__:
            print("There is a relation defined %s with Key: %r" % (cls.__name__, r))

            if hasattr(r.target, 'fullname') and r.target.fullname.endswith("version"):
                continue

            if r.key in backrefs:
                continue

            key = r.key
            target = ""
            if hasattr(r.target, 'fullname') and r.target.fullname in versioned_tables:
                target = r.mapper.entity.__name__ + "Live"
            else:
                if r.direction == MANYTOONE:
                    args[key] = db.relationship(r.mapper)
                elif r.direction == MANYTOMANY:
                    # if hasattr(r, 'secondary') and r.secondary:
                    #     print("SECONDARY for ... ", r)
                    #     kwargs['secondary'] = r.secondary
                    primaryjoin = copy.copy(r.primaryjoin)
                    primaryjoin.left = args[primaryjoin.left.key]
                    secondaryjoin = copy.copy(r.secondaryjoin)
                    args[key] = db.relationship(r.mapper,
                                                viewonly=True,
                                                primaryjoin=primaryjoin,
                                                foreign_keys=[primaryjoin.right, secondaryjoin.right],
                                                secondary=r.secondary,
                                                secondaryjoin=secondaryjoin
                                                )
                else:
                    primaryjoin = copy.copy(r.primaryjoin)
                    primaryjoin.left = args[primaryjoin.left.key]
                    args[key] = db.relationship(r.mapper,
                                                viewonly=True,
                                                primaryjoin=primaryjoin,
                                                foreign_keys=[primaryjoin.right])
                continue

            kwargs = {}
            if hasattr(r, "backref") and r.backref:
                backref_key = r.backref[0]
                backrefs.append(backref_key)
                backref = r.backref[1]
                remote_side = None
                if hasattr(backref["remote_side"].cls, "LiveType") or backref["remote_side"].cls == cls:
                    orig_arg = backref["remote_side"].arg
                    arg_v = orig_arg.split(".")
                    arg_v[0] += "Live"
                    remote_side = ".".join(arg_v)
                    kwargs['backref'] = db.backref(backref_key, remote_side=remote_side)


            args[key] = db.relationship(target, cascade="none, ", **kwargs)

    if args.get("before_insert"): del args["before_insert"]
    if args.get("before_update"): del args["before_update"]
    if args.get("__versioned__"): del args["__versioned__"]

    args["template"] = getattr(cls, "template") if hasattr(cls, "template") else ""

    mapper_args = {}
    if hasattr(cls, "__mapper_args__"):
        mapper_args = cls.__mapper_args__

    args['__versioned_draft_class__'] = cls
    args['__create_live__'] = False

    cls.LiveType = type(
        '%sLive' % cls.__name__,
        baseclass,
        args
    )

    cls.LiveType.__create_live__ = False

    for key, arg in mapper_args.items():
        if key == "polymorphic_on":
            mapper_args[key] = table.columns[arg]

    live_mapper = mapper(cls, cls.LiveTable,
                         non_primary=True,
                         **mapper_args)

    cls.live_mapper = live_mapper
    return cls.LiveTable


class VersionedMixin(object):
    """
    A mixin that adds versioning support to DataObjects.
    It adds a new live table that saves the object on a publish operation,
    a new query_live operator that queries the live versions of the object
    and a versions relationship that saves all versions of this object (a version
    is automatically created on a save operation).
    """
    __versioned__ = {
        'base_classes': (db.Model, )
    }

    __create_live__ = True

    # query_class = VersionedQuery

    @classproperty
    def query_live(cls):
        """
        Query the live version of this DataObject
        """
        return cls.LiveType.query

    @classmethod
    def query_factory(cls, stage="live"):
        if stage == "live":
            return super(cls.LiveType).query_factory()
        else:
            return super(cls).query_factory()

    @classmethod
    def live_table(cls):
        return cls.__tablename__ + "_live"

    def get_published(self):
        return self

    def can_publish(self):
        """
        Override this function to control who is allowed to publish
        pages in the CMS
        :return: Boolean (True if allowed to publish)
        """
        return True


    def mark_as_published(self):
        """
        Create a copy of the current draft to the live table and
        publish this DataObject (make it visible to the outside world).
        :return: empty
        """
        if not self.can_publish():
            return False
        if not self.id:
            raise Exception("No ID set!")
        logger.debug('Publishing Page with ID: %s', str(self.id))

        live_table_name = self.live_table()

        t = self.LiveType
        t_obj = db.session.query(t).get(self.id)
        new_object = False
        if not t_obj:
            t_obj = t()
            new_object = True

        ins = sainspect(self.__class__)

        for column in ins.columns:
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
        if not cls.__table__.name in versioned_tables:
            if not (mapper.inherits and mapper.inherits.tables[0].name in versioned_tables):
                versioned_tables.append(cls.__table__.name)
                versioned_classes.append(cls.__name__)


@event.listens_for(mapper, 'after_configured')
def after_configured():
    for cls in classes_to_create:
        live_table = create_live_table(cls)
        cls.live_table_instance = live_table
    classes_to_create.clear()


import sqlalchemy as sa
sa.orm.configure_mappers()