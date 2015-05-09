Tutorial
========

This tutorial is trying to give a quick introduction in how to create your first website with SilverFlask.

Creating a simple page type
-------------------------

First, we will create a basic page type for our website. Therefore we need to subclass :class:`silverflask.models.SiteTree`:

::

    from silverflask.models import SiteTree

    class SimplePage(SiteTree):
        db = {
            "content": "UnicodeText"
        }

Now you should point your browser to `localhost:5000/admin/dev/build`_ to automatically
generate the necessary database entries for you.

When you open `admin`_ and check the "Add Pages" menu, you will
see our SimplePage as one of the available page types. You can even start
editing the page, save and publish it and it should render just fine in the
default template. Note that all of this functionality comes from the SiteTree

This is because we chose the name ``content`` for our db field, which is also
the standard name for the main content which is used in the default template.

We can also create a little script to create a new instance of this page:

::

    from silverflask import db

    sp = SimplePage()
    sp.name = "What a beautiful title"
    sp.content = "Interesting Content"
    db.session.add(sp)
    db.session.commit(sp)

This example also shows how the variables defined in ``db`` are added to the class
namespace and are accessible through their names.

All column types from sqlalchemy are available, such as

* Integer
* Text
* String (text, but with a maximum length)
* Boolean
* Date, and DateTime
* ... (check sqla_types_. for more)

Extending the page further
------------------------

Suppose we want to add a cute little header image to the page, we can do that
easily by adding a ``has_one`` relation to the ``SimplePage``. The relation
will point to the :class:`silverflask.models.ImageObject`.

::

    from silverflask.models import SiteTree

    class SimplePage(SiteTree):
        db = {
            "content": "UnicodeText"
        }
        has_one = {
            "header_image": "ImageObject"
        }

The necessary database columns for this relation are automatically added to
the model.

Now you might wonder how to access this image -- it's easy. Relations are



.. _sqla_types: http://docs.sqlalchemy.org/en/latest/core/type_basics.html
.. _localhost:5000/admin/dev/build: http://localhost:5000/admin/dev/build
.. _admin: http://localhost:5000/admin
