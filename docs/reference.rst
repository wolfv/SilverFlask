Reference
=======

DataObject
-----
.. automodule:: silverflask.models.DataObject
    :members:


SiteTree
----

.. automodule:: silverflask.models.SiteTree
    :members:

Mixins
------

Silverflask defines a number of mixins that can be utilized to enhance DataObjects (and are used in the SiteTree class for example).

.. automodule:: silverflask.mixins.OrderableMixin
    :members:

.. automodule:: silverflask.mixins.PolymorphicMixin
    :members:

.. automodule:: silverflask.mixins.VersionedMixin
    :members:


User
----

.. automodule:: silverflask.models.User
    :members:


FileObject
-----

The file objects reflect the file items uploaded through the CMS. ImageObject is an inherited class which implements common image functionality, such as cropping and resizing.

.. automodule:: silverflask.models.FileObject
    :members:

.. automodule:: silverflask.models.ImageObject
    :members:


FileStorageBackend
-----

The `FileStorageBackend` is a class that abstracts away the underlying file storage. At the moment, the only implemented backend is the `LocalFileStorageBackend` which implements methods to save files to the local flask installation (defaults to the `/static/uploads/` folder).

Another FileStorageBackend could, for example, be an implementation for a S3 Backend (e.g. using the boto library).


