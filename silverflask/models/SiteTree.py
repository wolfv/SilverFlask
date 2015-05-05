from flask import abort, current_app, url_for
from slugify import slugify

from silverflask import db
from silverflask.models import DataObject
from silverflask.mixins import OrderableMixin, VersionedMixin, PolymorphicMixin


class SiteTree(VersionedMixin, PolymorphicMixin, OrderableMixin, DataObject, db.Model):
    """
    The SiteTree is the database model from which all pages have to inherit.
    It defines the parent/children relationships of the page tree.
    It also defines everything that's needed to get nice URL slugs working.
    """

    parent_id = db.Column(db.Integer, db.ForeignKey('sitetree.id'))
    name = db.Column(db.String)
    urlsegment = db.Column(db.String(250), nullable=False)

    template = "page.html"

    children = db.relationship('SiteTree',
                               cascade="all",
                               # many to one + adjacency list - remote_side
                               # is required to reference the 'remote'
                               # column in the join condition.
                               backref=db.backref("parent", remote_side='SiteTree.id'),
                               order_by='SiteTree.sort_order'
    )

    allowed_children = []
    can_be_root = True
    icon = 'glyphicon glyphicon-file'

    def get_siblings(self):
        return SiteTree.query.filter(SiteTree.parent_id == self.parent_id)

    @classmethod
    def default_template(cls):
        return cls.__name__.lower() + ".html"

    def parents(self):
        tree_el = self.parent
        parents = []
        while tree_el:
            parents.append(tree_el)
            tree_el = tree_el.parent
        return parents

    @staticmethod
    def get_sitetree(parent_id=None):
        base_page = SiteTree.query.filter(SiteTree.parent_id == parent_id)\
                                  .order_by(SiteTree.sort_order.asc())
        dest_list = []
        for p in base_page:
            dest_dict = {}
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
        return form

    def append_child(self, child):
        self.children.append(child)

    def parent_at_level(self, level=1):
        level = level - 1
        parents = self.parents()
        n_parents = len(parents)
        if n_parents > level:
            return parents[level]
        if n_parents == level:
            return self
        else:
            return False

    def menu(self, level=1):
        # This returns the menu with
        # self as reference
        level = level - 1
        parents = self.parents()
        n_parents = len(parents)
        if n_parents > level:
            cls = self.__class__
            level_parent = parents[level]
            result = cls.query.filter(cls.parent_id == level_parent.id).all()
            return result
        if n_parents == level:
            return self.children
        else:
            return False

    def as_dict(self):
        d = dict()
        try:
            d = super().as_dict()
        except Exception as e:
            """
            This is due to problems with wsgi and reloading:
            http://stackoverflow.com/questions/9722343/python-super-behavior-not-dependable
            """
            for c in self.__class__.mro():
                if c != self.__class__:
                    super_object = super(c, self)
                    if hasattr(super_object, 'as_dict'):
                        d.update(super_object.as_dict())
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
            "type": self.__class__.__name__,
            "li_attr": {
                "data-pageid": str(self.id)
            },
            "a_attr": {
                "href": url_for("PagesCMSController.edit_page", page_id=self.id)
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
        if self.urlsegment == current_app.config["SILVERFLASK_HOME_URLSEGMENT"]:
            return "/"
        self_url = "/" + self.urlsegment
        url = ""
        el = self

        while el.parent:
            url = "/" + el.parent.urlsegment
            el = el.parent
        url += self_url
        return url


    def set_parent(self, parent_id):
        if not parent_id:
            if self.can_be_root:
                self.parent_id = None
                return
            else:
                raise Exception("This page type can not be a root node!")
        else:
            parent = SiteTree.query.get(int(parent_id))
            if parent:
                if hasattr(parent, 'allowed_children') and self.__class__.__name__ in parent.allowed_children:
                    self.parent_id = parent_id
                else:
                    raise Exception("Parent not allowed!")
            else:
                raise Exception("Parent not existing!")
        return

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

    @classmethod
    def pagetypes(cls):
        polymorphic_map = cls.__mapper__.polymorphic_map
        sitetree_props = {}
        for mapper in polymorphic_map.values():
            if mapper.class_ != cls:
                mapped_class = mapper.class_
                sitetree_props[mapped_class.__name__] = {
                    'allowed_children': mapped_class.allowed_children,
                    'icon': mapped_class.icon if mapped_class.icon else 'default'
                }
        return sitetree_props

    @classmethod
    def before_insert(cls, mapper, context, target):
        target.create_slug(target)

    @classmethod
    def before_update(cls, mapper, context, target):
        target.create_slug(target, target.id)