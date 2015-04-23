from flask.ext.sqlalchemy import SQLAlchemy, Model
from sqlalchemy import orm
from sqlalchemy.exc import CompileError
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
            if mapper:
                query = type.query_class(mapper, session=self.sa.session())
                if hasattr(type, 'default_order') and type.default_order is not None:
                    default_order = type.default_order.split()
                    col = default_order[0]
                    direction = None
                    if len(default_order) > 1:
                        direction = default_order[1]
                        assert direction == "ASC" or direction == "DESC"
                    if direction == "ASC":
                        query = query.order_by(mapper.c[col].asc())
                    else:
                        query = query.order_by(mapper.c[col].desc())
                return query
        except UnmappedClassError:
            return None


class SQLAlchemy(SQLAlchemy):
    def make_declarative_base(self):
        base = declarative_base(cls=Model, name='Model',
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base
