from silverflask import db
from sqlalchemy import func

class OrderableMixin(object):
    """
    A mixin that makes a DataObject sortable by adding a sort_order database field.
    Classes with this mixin automatically keep the sort_order in sync.
    """
    sort_order = db.Column(db.Integer, nullable=False, default=1)

    default_order = "sort_order ASC"

    def insert_after(self, index, orderable_base_class=None, index_absolute=True, query=None):
        """
        Inser after index variable

        :param index: index (this is the sort_order variable of the element that you want to insert after!)
        :param orderable_base_class: baseclass (useful in certain circumstances e.g. gridfields)
        :return: nothing
        """
        if orderable_base_class:
            cls = orderable_base_class
        else:
            cls = self.__class__
        cls.check_duplicates()
        query = query if query else db.session.query(cls)
        if not index_absolute:
            index_el = query.order_by(cls.sort_order.asc()).limit(1).offset(index).scalar()
            sort_order_index = index_el.sort_order

        db.session.query(cls)\
            .filter(cls.sort_order > sort_order_index)\
            .update({cls.sort_order: cls.sort_order + 1})

        self.sort_order = index + 1

        if hasattr(cls, 'LiveType'):
            # Repeat the same for the live version of the page
            cls = cls.LiveType
            cls.check_duplicates()
            live_self = cls.query.get(self.id)
            live_self.check_duplicates()
            db.session.commit()

            query = db.session.query(cls)
            if not index_absolute:
                print(query)
                print(index)
                print(str(query.order_by(cls.sort_order.asc()).limit(1).offset(index)))
                print(query.order_by(cls.sort_order.asc()).all())
                index_el = query.order_by(cls.sort_order.asc()).limit(1).offset(index).scalar()
                index = index_el.sort_order

            db.session.query(cls) \
                .filter(cls.sort_order > index) \
                .update({cls.sort_order: cls.sort_order + 1})
            live_self.sort_order = index + 1


    @classmethod
    def reindex(cls):
        """
        Reindexes the table.

        The sort order field can have "jumps" in it (e.g. 1, 4, 5, 8, 9) and reindex brings that back
        to a linearly ascending order: (1,2,3,4...)
        """
        for index, el in enumerate(db.session.query(cls).order_by(cls.sort_order.asc())):
            el.sort_order = index
        db.session.commit()

    @classmethod
    def check_duplicates(cls):
        """
        Check the table for duplicates and if there are duplicates reindex
        :return: nothing
        """
        duplicates = db.session.query(cls).group_by(cls.sort_order)\
                               .having(func.count(cls.id) > 1).count()
        if duplicates > 0:
            cls.reindex()

    def move_after(self, obj):
        """
        Move current DataObject after index (= sort_order) of another element

        :param index: obj element where to move after or sort order of other elements
        :return: nothing
        """
        if hasattr(obj, 'sort_order'):
            self.insert_after(obj.sort_order)
        else:
            _id = int(obj)
            if _id <= 0:
                sort_order = 0
            else:
                sort_order = db.session.query(self.__class__).get(_id).sort_order
            self.insert_after(sort_order)


    @classmethod
    def before_insert(cls, mapper, connection, target):
        target.init_order()

    def init_order(self):
        """
        Sort element to the end
        """
        cls = self.__class__
        if not self.sort_order:
            query = db.session.query(func.max(cls.sort_order))
            v = query[0]
            if v[0]:
                self.sort_order = v[0] + 1
            else:
                self.sort_order = 1