#! ../env/bin/python
# -*- coding: utf-8 -*-
from silverflask import create_app
from silverflask import db
from silverflask.models import Page, User, SiteTree
import unittest
import tempfile
from flask.ext.testing import TestCase

class BaseTest(TestCase):
    def create_app(self):
        self.app = create_app("silverflask.settings.TestConfig", env="dev")
        return self.app

