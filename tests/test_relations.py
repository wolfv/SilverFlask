from silverflask import create_app
from silverflask import db
from silverflask.models import DataObject, User
from test_base import BaseTest

class A(DataObject, db.Model):
    db = {
        "text": "UnicodeText"
    }
    many_many = {
        "snips": "Snippet",
        "snipstwo": "Snippet",
    }

    has_one = {
        "snip": "Snippet"
    }

    has_many = {
        "imgs": "Img"
    }

class Img(DataObject, db.Model):
    db = {
        "caption": "String"
    }
    has_one = {
        "A": "A"
    }

class B(DataObject, db.Model):
    db = {
        "text": "UnicodeText"
    }
    many_many = {
        "snips": "Snippet",
    }

class Snippet(DataObject, db.Model):
    db = {
        "caption": "String"
    }
    belongs_many_many = {
        "As": "A.snips",
        "Azwos": "A.snipstwo",
        "Bs": "B"
    }

    def __init__(self, caption):
        self.caption = caption

class TestRelations(BaseTest):
    def create_app(self):
        self.app = create_app("silverflask.settings.TestConfig", env="dev")
        return self.app

    def setUp(self):
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()
        pass
    def teardown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def test_relations(self):
        print("SNIPS: ", B.snips, type(B.snips))
        a = B()
        a.text = "Test"

        s1 = Snippet("s1")
        s2 = Snippet("s2")

        a.snips.append(s1)
        a.snips.append(s2)

        db.session.add(a)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        a_db = B.query.one()

        assert self.deepequal(a_db.snips, [s1, s2])
        print(a_db.snips)

        snippet_1 = Snippet.query.filter(Snippet.caption == "s1").one()
        print(snippet_1.Bs)
        assert snippet_1.Bs[0] == a_db


        a = A()
        a.text = "asdasd"

        a.snips.append(s1, s2)
        a.snipstwo.append(s2)

        db.session.add(a)
        db.session.commit()

        a_db = A.query.first()

        print(a_db.snips)
        print(a_db.snipstwo)

        assert(self.deepequal(a_db.snipstwo, [s2]))
        assert(self.deepequal(a_db.snips, [s1, s2]))

        img = Img()
        img.caption = "text1"
        a.imgs.append(img)
        img2 = Img()
        img2.caption = "text2"
        a.imgs.append(img2)
        db.session.add(img)
        db.session.add(img2)

        db.session.commit()

        a_db = A.query.first()
        img_db = Img.query.first()
        print(a_db.imgs)
        print(img_db.A)
        assert(img_db.A == a_db)
        assert(self.deepequal(a_db.imgs, [img, img2]))
