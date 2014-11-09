# Stolen from https://gist.github.com/dtheodor/55325741f04f7d64daa5
# by github.com/dtheodor

from sqlalchemy_continuum import get_versioning_manager, make_versioned, \
    versioning_manager, version_class, transaction_class
from sqlalchemy_continuum.utils import version_obj
from sqlalchemy_continuum.plugins import TransactionMetaPlugin
from silverflask import db

meta_plugin = TransactionMetaPlugin()

make_versioned(plugins=[meta_plugin])

class VersionedMixin(object):
    """Base class for SQL Alchemy continuum objects that supports tagging"""
    __versioned__ = {
        'base_classes': (db.Model, )
    }

    def tag_current_transaction(self, **kwargs):
        """Add keyword arguments that will be stored as a `TransactionMeta`
        entry on next successful commit that includes versioned objects.
        """
        # existing_tx_meta = get_versioning_manager(cls).uow.tx.meta
        uow = versioning_manager.unit_of_work(db.session)
        tx = uow.create_transaction(db.session)
        tx.meta = {u'published': u'true'}
        db.session.commit()
        # existing_tx_meta = version_obj(db.session, self).tx.meta
        # for k in kwargs.keys():
        #     if k in existing_tx_meta:
        #         raise KeyError(
        #            "Key '{}' already exists in transaction meta ".format(k) +
        #            "key-value pairs: '{}'".format(existing_tx_meta))
        # existing_tx_meta.update(**kwargs)
        
    def remove_tags(self, **kwargs):
        """Delete all found key-value tags from any transaction"""
        TransactionMeta = get_versioning_manager(self).transaction_meta_cls
        session = db.session
        transaction_meta_filter = []
        for key, value in kwargs.items():
            transaction_meta_filter.extend([TransactionMeta.key == key,
                                            TransactionMeta.value == str(value)])
        #just delete them
        session.query(TransactionMeta).filter(*transaction_meta_filter).delete()


    def get_tagged_version(self, **kwargs):
        """Return a query on the version objects that are associated with the
        transactions tagged with the `kwargs`. The `kwargs` values will be
        converted to strings to construct the key/value query.
        """
        TransactionMeta = get_versioning_manager(self).transaction_meta_cls
        session = db.session
        Transaction = transaction_class(self.__class__)
        Version = version_class(self.__class__)

        transaction_meta_filter = []
        for key, value in kwargs.items():
            #convert value to string, TransactionMeta stores strings
            transaction_meta_filter.extend([TransactionMeta.key == key,
                                            TransactionMeta.value == str(value)])
        object_query = session.query(Version
            ).join(Transaction,
                   Transaction.id == Version.id
            ).join(TransactionMeta,
                   Transaction.id == TransactionMeta.transaction_id
            ).filter(*transaction_meta_filter)
        return object_query

    def get_published(self):
        return self.get_tagged_version(article_published=self.id).scalar()

    def mark_as_published(self):
        #remove older tags if you want to support only 1 published version
        self.remove_tags(article_published=self.id)
        self.tag_current_transaction(article_published=self.id)

import sqlalchemy as sa
sa.orm.configure_mappers()