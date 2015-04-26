from flask.ext.sqlalchemy import SQLAlchemy, Model
from sqlalchemy import orm
from sqlalchemy.exc import CompileError
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from silverflask.modelbuilder import get_column
from sqlalchemy import event
import sqlalchemy
from sqlalchemy.orm import mapper

import types

page_attr = ["default_sort", "template", "get_cms_form"]

def merge_dicts(d1, d2):
    res = d2.copy()
    res.update(d1)
    return res


class _BoundDeclarativeMeta(DeclarativeMeta):

    def __new__(cls, name, bases, d):
        if d.get("__abstract_inherit__"):
            inherit = d['__abstract_inherit__'][0].__dict__
            d['super'] = {}
            for key in inherit:
                if hasattr(inherit[key], '__module__'):
                    module = str(inherit[key].__module__)
                    if module.startswith('sqlalchemy'):
                        continue
                if key not in d:
                    d[key] = inherit[key]
                elif key in d and type(inherit[key]) == types.FunctionType:
                    if not d['super'].get(key):
                        d['super'][key] = list()
                    d['super'][key].append(inherit[key])


        return DeclarativeMeta.__new__(cls, name, bases, d)

    @staticmethod
    def get_assoc_tablename(from_cls, from_key, to):
        from_key = '_' + from_key if from_key else ''
        return "assoc_" + from_cls.lower() + from_key.lower() + "_" + to.lower()

    @staticmethod
    def get_assoc_tablename_backref(from_cls, to):
        return "assoc_" + from_cls.replace(".", "_").lower() + "_" + to.lower()

    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        abstract_inherit = d.get("__abstract_inherit__")
        if abstract_inherit:
            inherit = d['__abstract_inherit__'][0].__dict__
            d['super'] = {}
            for key in inherit:
                if hasattr(inherit[key], '__module__'):
                    module = str(inherit[key].__module__)
                    if module.startswith('sqlalchemy'):
                        continue
                if key not in d:
                    d[key] = inherit[key]
                elif key in d and type(inherit[key]) == types.FunctionType:
                    if not d['super'].get(key):
                        d['super'][key] = list()
                    d['super'][key].append(inherit[key])


        db = {}
        has_one = {}
        has_many = {}

        many_many = {}
        belongs_many_many = {}

        if abstract_inherit:
            for b in reversed(abstract_inherit):
                if hasattr(b, 'db'):
                    db = merge_dicts(db, b.db)
                if hasattr(b, 'has_one'):
                    has_one = merge_dicts(has_one, b.has_one)
                if hasattr(b, 'has_many'):
                    has_many = merge_dicts(has_many, b.has_many)
                if hasattr(b, 'many_many'):
                    many_many = merge_dicts(many_many, b.many_many)
                if hasattr(b, 'belongs_many_many'):
                    belongs_many_many = merge_dicts(belongs_many_many, b.belongs_many_many)

        if d.get('db'):
            db.update(d.get('db'))
        if d.get('has_one'):
            has_one.update(d.get('has_one'))
        if d.get('has_many'):
            has_many.update(d.get('has_many'))
        if d.get('many_many'):
            many_many.update(d.get('many_many'))
        if d.get('belongs_many_many'):
            belongs_many_many.update(d.get('belongs_many_many'))

        if db:
            for key in db:
                if type(db[key]) == str:
                    col = sqlalchemy.Column(getattr(sqlalchemy, db[key]))
                else:
                    v = db[key]
                    t = v['type']
                    fk = v.get('foreign_key')
                    pk = v.get('primary_key') if v.get('primary_key') else False
                    col = sqlalchemy.Column(getattr(sqlalchemy, t), sqlalchemy.ForeignKey(fk), primary_key=pk)

                setattr(self, key, col)

        for key in has_one:
            ref = has_one[key]
            rel = sqlalchemy.orm.relationship(ref)
            col = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(ref.lower() + ".id"))
            setattr(self, key + "_id", col)
            setattr(self, key, rel)

        for key in has_many:
            ref = has_many[key]
            rel = sqlalchemy.orm.relationship(ref)
            setattr(self, key, rel)

        for key in belongs_many_many:
            ref = belongs_many_many[key]
            split_ref = ref.split(".")
            many_many_cls = split_ref[0]
            table_name = self.get_assoc_tablename_backref(ref, self.__name__)
            rel = sqlalchemy.orm.relationship(many_many_cls, secondary=table_name)
            setattr(self, key, rel)

        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key

        many_many_values = list(many_many.values())
        many_many_duplicates = [x for x in many_many_values if many_many_values.count(x) > 1]
        self.assoc_tables = []
        for key in many_many:
            ref = many_many[key]
            fk2 = ref.lower() + ".id"
            if ref in many_many_duplicates:
                table_name = self.get_assoc_tablename(self.__name__, key, ref)
            else:
                table_name = self.get_assoc_tablename(self.__name__, '', ref)

            table = sqlalchemy.Table(table_name, self.metadata,
                                                sqlalchemy.Column(name.lower() + '_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(name.lower() + '.id')),
                                                sqlalchemy.Column(ref + '_id', sqlalchemy.Integer, sqlalchemy.ForeignKey(fk2)))

            self.assoc_tables.append(table)
            rel = sqlalchemy.orm.relationship(ref, secondary=table_name)
            setattr(self, key, rel)


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