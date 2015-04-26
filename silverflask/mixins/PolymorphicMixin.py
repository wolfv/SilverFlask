#
# Polymorphic Mixins
#
from silverflask import db
from sqlalchemy.ext.declarative import declared_attr
from silverflask.helper import classproperty


class PolymorphicMixin(object):
    type = db.Column(db.String(50))

    @declared_attr
    def __mapper_args__(cls):
        if hasattr(cls, '__versioned_draft_class__'):
            # Use same identities as draft class
            ident = cls.__versioned_draft_class__.__mapper_args__["polymorphic_identity"]
        else:
            ident = cls.__tablename__
        d = {
            'polymorphic_identity': ident,
        }
        # this is a base object, therefore we are not
        # redefining the column on which it is polymorphic

        if hasattr(cls.__table__.columns, 'id') and not cls.__table__.columns.id.foreign_keys:
            d['polymorphic_on'] = 'type'
        return d

