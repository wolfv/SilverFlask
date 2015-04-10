#! ../env/bin/python
# -*- coding: utf-8 -*-
from test_base import BaseTest
from silverflask import db
from silverflask.models import User

class TestVersioning(BaseTest):
    def setUp(self):
        super().setUp()
        admin = User('admin_dos', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_user_login(self):
        rv = self.client.post("user/sign-in?next=/admin", data=dict(
            username='admin_dos',
            password="supersafepassword"
        ), follow_redirects=True)

        assert rv.status_code == 200 # redirect
        rv = self.client.get("user/sign-out", follow_redirects=True)
        assert rv.status_code == 200

        rv = self.client.post("user/sign-in", data=dict(
            username='admin_dos',
            password="wrongpass",
        ), follow_redirects=True)

        assert rv.status_code == 200 # no page change
        self.assertIn("Incorrect Username", rv.data.decode("utf-8"))
