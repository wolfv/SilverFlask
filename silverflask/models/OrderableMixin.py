from sqlalchemy.ext.declarative import declared_attr
from silverflask import db
from sqlalchemy import func, text

class OrderableMixin(object):
    sort_order = db.Column(db.Integer, nullable=False, default=1)

    @classmethod
    def query_factory(cls):
        # query = super().query
        return db.session.query(cls).order_by(cls.sort_order.asc())

    def insert_after(self, index, orderable_base_class=None):
        if orderable_base_class:
            cls = orderable_base_class
        else:
            cls = self.__class__
        cls.check_duplicates()
        db.session.query(cls)\
            .filter(cls.sort_order >= index)\
            .update({cls.sort_order: cls.sort_order + 1})
        self.sort_order = index

    @classmethod
    def reindex(cls):
        print("Reindexing!")
        print(cls)
        for index, el in enumerate(db.session.query(cls).order_by(cls.sort_order.asc())):
            el.sort_order = index
        db.session.commit()

    @classmethod
    def check_duplicates(cls):
        duplicates = db.session.query(cls).group_by(cls.sort_order)\
                               .having(func.count(cls.id) > 1).count()
        if duplicates > 0:
            cls.reindex()

    def move_after(self, index):
        self.insert_after(index)

    def init_order(self, cls):
        if not self.sort_order:
            query = db.session.query(func.max(cls.sort_order))
            v = query[0]
            if v[0]:
                self.sort_order = v[0] + 1
            else:
                self.sort_order = 1