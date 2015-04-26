#! ../env/bin/python
# -*- coding: utf-8 -*-
from silverflask import db
from tests.test_base import BaseTest
from silverflask.models import DataObject
from silverflask.mixins import OrderableMixin

class OrderedItem(OrderableMixin, DataObject, db.Model):
    def __repr__(self):
        return "<OrderedItem id: %s, sort_order: %s>" % (self.id, self.sort_order)


class TestOrdering(BaseTest):
    def teardown(self):
        pass
        # db.drop_all()
        # db.session.remove()

    def test_ordering(self):
        o1 = OrderedItem()
        db.session.add(o1)
        db.session.commit()
        o2 = OrderedItem()
        db.session.add(o2)
        db.session.commit()
        print(OrderedItem.singular_name, OrderedItem.plural_name)
        assert OrderedItem.default_order is not None
        assert(o1.sort_order == 1)
        assert(o2.sort_order == 2)

        o1.insert_after(o2.sort_order)
        db.session.commit()
        print(o1.sort_order)
        assert(o1.sort_order == 3)
        print(OrderedItem.query.all())
        assert self.deepequal(OrderedItem.query.all(), [o2, o1])

        o2.insert_after(o1.sort_order)
        db.session.commit()
        assert self.deepequal(OrderedItem.query.all(), [o1, o2])

        o3 = OrderedItem()
        db.session.add(o3)
        db.session.commit()

        assert self.deepequal(OrderedItem.query.all(), [o1, o2, o3])

        o3.insert_after(0)
        db.session.commit()
        assert self.deepequal(OrderedItem.query.all(), [o3, o1, o2])

