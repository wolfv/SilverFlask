from flask.ext.sqlalchemy import SQLAlchemy, Model
from sqlalchemy import orm, event
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

class _BoundDeclarativeMeta(DeclarativeMeta):

    def __new__(cls, name, bases, d):
        return DeclarativeMeta.__new__(cls, name, bases, d)

    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key


class _QueryProperty(object):

    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            print(type)
            if mapper:
                query = type.query_class(mapper, session=self.sa.session())
                if hasattr(type, 'default_sort'):
                    query.order_by(type.default_sort)
                return query
        except UnmappedClassError:
            return None


class SQLAlchemy(SQLAlchemy):
    def make_declarative_base(self):
        base = declarative_base(cls=Model, name='Model',
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base
