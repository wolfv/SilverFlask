from .DataObject import DataObject
from flask import abort
from slugify import slugify
from .OrderableMixin import OrderableMixin
from sqlalchemy import event

from silverflask import db


class SiteTree(DataObject, OrderableMixin, db.Model):
    parent_id = db.Column(db.Integer, db.ForeignKey('sitetree.id'))
    name = db.Column(db.String)
    database = ["parent_id", "name"]
    type = db.Column(db.String(50))
    urlsegment = db.Column(db.String(250), nullable=False)

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
        d = super().as_dict()
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
    def get_by_url(url):
        vars = url.split('/')
        node = SiteTree.query.filter(SiteTree.urlsegment == vars[0]).first()
        if not node:
            abort(404)

        for var in vars[1:]:
            node = SiteTree.query.filter(SiteTree.urlsegment == var,
                                         SiteTree.parent_id == node.id).first()
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

    @staticmethod
    def get_slug_for_string(name):
        return slugify(name)

    def set_parent(self, parent_id):
        self.parent_id = parent_id

    def __init__(self):
        self.database.extend(super(SiteTree, self).database)

    def before_insert(self, mapper, context, target):
        possible_slug = slugify(target.name)
        slug = possible_slug
        count = 0
        while self.query.filter(self.parent_id == target.parent_id,
                                self.urlsegment == slug).count():
            slug = "{0}-{1}".format(possible_slug, count)
        target.urlsegment = slug
