#! ../env/bin/python
# -*- coding: utf-8 -*-
from test_base import BaseTest
from silverflask import db
from silverflask.models import User

class TestVersioning(BaseTest):
    def setUp(self):
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_user_login(self):
        rv = self.client.post('/admin/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)

        assert rv.status_code == 200
        assert 'Logged in successfully.' in rv.data
