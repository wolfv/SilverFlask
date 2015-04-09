from .DataObject import DataObject
from flask import abort
from slugify import slugify
from .OrderableMixin import OrderableMixin
from .VersionedMixin import VersionedMixin
from sqlalchemy import event

from silverflask import db


class SiteTree(VersionedMixin, DataObject, OrderableMixin, db.Model):
    """
    The SiteTree is the database model from which all pages have to inherit.
    It defines the parent/children relationships of the page tree.
    It also defines everything that's needed to get nice URL slugs working.
    """

    parent_id = db.Column(db.Integer, db.ForeignKey('sitetree.id'))
    name = db.Column(db.String)
    database = ["parent_id", "name"]
    type = db.Column(db.String(50))
    urlsegment = db.Column(db.String(250), nullable=False)

    template = "page.html"

    __mapper_args__ = {
        'polymorphic_identity': 'sitetree',
        'polymorphic_on': type
    }

    children = db.relationship('SiteTree',
                               cascade="all",
                               # many to one + adjacency list - remote_side
                               # is required to reference the 'remote'
                               # column in the join condition.
                               backref=db.backref("parent", remote_side='SiteTree.id'),
    )

    allowed_children = []

    def get_siblings(self):
        return SiteTree.query.filter(SiteTree.parent_id == self.parent_id)

    @classmethod
    def default_template(cls):
        return cls.__name__.lower() + ".html"

    @staticmethod
    def get_sitetree():
        base_page = SiteTree.query.filter(SiteTree.parent_id == None)
        dest_list = []
        for p in base_page:
            dest_dict = {}
            print(p.name)
            SiteTree.recursive_build_tree(p, dest_dict)
            dest_list.append(dest_dict)
        return dest_list

    @staticmethod
    def recursive_build_tree(root_node, dest_dict):
        dest_dict.update(root_node.jqtree_dict())
        children = root_node.children
        if children:
            dest_dict['children'] = []
            for child in children:
                temp_dict = {}
                dest_dict['children'].append(temp_dict)
                SiteTree.recursive_build_tree(child, temp_dict)
        else:
            return


    @classmethod
    def get_cms_form(cls):
        form = super().get_cms_form()
        del form.children
        del form.sort_order
        del form.urlsegment
        return form

    def append_child(self, child):
        self.children.append(child)

    def as_dict(self):
        d = dict()
        try:
            d = super().as_dict()
        except:
            d = super(self.__class__, self).as_dict()
        d.update({
            "parent_id": self.parent_id,
            "name": self.name,
            "type": self.type
        })
        return d

    def jqtree_dict(self):
        return {
            "text": self.name,
            "parent_id": self.parent_id,
            "created_on": self.created_on,
            "li_attr": {
                "data-pageid": str(self.id)
            },
            "a_attr": {
                "href": "/admin/edit/page/{0}".format(self.id)
            }
        }

    @staticmethod
    def get_by_url(url, cls=None):
        if not cls:
            cls = SiteTree
        vars = url.split('/')
        node = cls.query.filter(cls.urlsegment == vars[0]).first()
        if not node:
            abort(404)

        for var in vars[1:]:
            node = cls.query.filter(cls.urlsegment == var,
                                    cls.parent_id == node.id).first()
            if not node:
                abort(404)
        return node

    def get_url(self):
        url = "/" + self.urlsegment
        el = self
        while el.parent:
            url = "/" + el.parent.url_segment  + url
            el = el.parent
        return url


    def set_parent(self, parent_id):
        self.parent_id = parent_id

    def __init__(self):
        pass
        # self.database.extend(super(SiteTree, self).database)

    @classmethod
    def create_slug(cls, target, id=None):
        possible_slug = slugify(target.name, to_lower=True)
        slug = possible_slug
        count = 0
        def get_query(target, slug, id=None):
            query = cls.query.filter(cls.parent_id == target.parent_id,
                                     cls.urlsegment == slug)
            if id:
                query = query.filter(cls.id != id)
            return query
        while get_query(target, slug, id).count() > 0:
            slug = "{0}-{1}".format(possible_slug, count)
        target.urlsegment = slug

    def before_insert(self, mapper, context, target):
        self.create_slug(target)

    def before_update(self, mapper, context, target):
        self.create_slug(target, self.id)

    @property
    def stprop(self):
        return "WAHZUP?"