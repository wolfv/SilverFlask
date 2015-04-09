#! ../env/bin/python
# -*- coding: utf-8 -*-
from silverflask import create_app
from silverflask import db
from silverflask.models import Page, User, SiteTree
import unittest
import tempfile
from flask.ext.testing import TestCase

class TestVersioning(TestCase):
    def create_app(self):
        self.app = create_app("silverflask.settings.TestConfig", env="dev")
        return self.app

    def setUp(self):
        print("CREATING APP ..... .. ... ")
        # db.create_all()
        # db.create_all()
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()
        print(User.query.get(1).password)

    def teardown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def testversioning(self):

        assert Page.query_live.get_or_404 is not None

        # pass
        # with self.app.app_context():
        p = Page()
        p.name = "Test Page"
        p.content = "Voll Krazy"
        db.session.add(p)
        db.session.commit()
        #
        assert len(p.versions.all()) == 1

        assert Page.LiveType.query.filter(Page.name == "Test Page").first() == None
        assert Page.query_live.get(1) == None

        p.mark_as_published()
        db.session.commit()


        assert Page.LiveType.query.filter(Page.name == "Test Page").first() is not None

        p.name = "Test 123"
        db.session.commit()

        assert Page.LiveType.query.first().name == "Test Page"
        print(Page.LiveType.query.first().name)

        assert Page.query.first().name == "Test 123"
        p.mark_as_published()
        assert Page.LiveType.query.first().name == "Test 123"
        assert(len(p.versions.all()) == 2)
        versions = p.versions.all()
        assert versions[0].name == "Test Page"
        assert versions[1].name == "Test 123"

        print(Page.LiveType.query.first().name)



if __name__ == "__main__":
    unittest.main()