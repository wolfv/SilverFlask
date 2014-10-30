from .DataObject import DataObject

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class SiteTree(DataObject, db.Model):
    __tablename__ = "sitetree"
    parent_id = db.Column(db.Integer, db.ForeignKey('sitetree.id'))
    name = db.Column(db.String)
    database = ["parent_id", "name"]
    type = db.Column(db.String(50))
    urlsegment = db.Column(db.String(250))
    sort = db.Column(db.Integer)

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
        dest_dict.update(root_node.to_dict())
        children = root_node.children
        if children:
            dest_dict['children'] = []
            for child in children:
                temp_dict = {}
                dest_dict['children'].append(temp_dict)
                SiteTree.recursive_build_tree(child, temp_dict)
        else:
            return

    def to_dict(self):
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

    def append_child(self, child):
        self.children.append(child)

    def set_parent(self, parent_id):
        self.parent_id = parent_id

    def __init__(self):
        self.database.extend(super(SiteTree, self).database)
