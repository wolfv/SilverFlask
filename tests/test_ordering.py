#! ../env/bin/python
# -*- coding: utf-8 -*-
from silverflask import db
from tests.test_base import BaseTest
from silverflask.models import DataObject
from silverflask.mixins import OrderableMixin

class OrderedItem(DataObject, OrderableMixin, db.Model):
    pass

def deepequal(l1, l2):
    for i in range(0, len(l1)):
        if l1[i] != l2[i]:
            return False
    return True

class TestOrdering(BaseTest):
    def teardown(self):
        pass
        # db.drop_all()
        # db.session.remove()

    def test_ordering(self):
        print("SAdkaJKJ J AJS D")
        o1 = OrderedItem()
        db.session.add(o1)
        db.session.commit()
        o2 = OrderedItem()
        db.session.add(o2)
        db.session.commit()
        assert(o1.sort_order == 1)
        print(o1.sort_order, o2.sort_order)
        assert(o2.sort_order == 2)
        o2.insert_after(o1.id)
        db.session.commit()
        OrderedItem.query.all()
        assert deepequal(OrderedItem.query.all(), [o2, o1])