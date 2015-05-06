SilverFlask
===========

SilverFlask aims to be the first full-featured CMS building on top of solid foundations such as Flask, SQLAlchemy, Jinja2, WTForms and a huge number of plugins built on top of these such as SQLAlchemy-continuum, Flask-User, Flask-Login and countless others.

SilverFlask aims to create an environment that is exceptionally friendly for newbies and experienced developers alike.

SilverFlask is partly named after SilverStripe, one of the best and fully-featured CMS's around in PHP land. However, for my taste it had a few shortcomings. Of course, PHP as a programming language is multitudes less pleasant than python. And unfortunately, SilverStripe is built around a framework that is more or less made only for the CMS. I personally don't like this tight coupling as the framework has not gotten much exposure outside of the SilverStripe CMS world.
On the other hand, Flask is a very mature framework, and python is a lovely programming language.

Installation
------------

.. warning:: SilverFlask is currently in a pre-alpha-stealth state. Don't use it for anything serious.
    That said, feel free to experiment with it as much as you'd like to!

- Clone repo: ``git clone https://github.com/wolfv/SilverFlask``
- Create a virtualenv: 
    - ``export VIRTUALENV_PYTHON=/usr/bin/python3`` (``export VIRTUALENV_PYTHON=/usr/local/bin/python3`` on OS X with `Homebrew <http://brew.sh/>`_). Only Python 3 is supported.
    - I like virtualenvwrapper, instructions for Ubuntu here: `Link <http://roundhere.net/journal/virtualenv-ubuntu-12-10/>`_
    - Toggle the virtualenv with ``workon <yourvirtualenvname>``
- When in the virtualenv, install all necessary packages via ``make requirements``
- Use the manage.py script to create the database (defaults to ``database.db`` in the app folder: ``python manage.py createdb``
- Start the application server by entering ``python manage.py runserver``
- Point your webbrowser to http://localhost:5000 to visit your first SilverFlask website

The basic building blocks
------

SilverFlask defines a number of basic building blocks for websites.

DataObject
-----
.. automodule:: silverflask.models.DataObject
    :members:



SiteTree
----

.. automodule:: silverflask.models.SiteTree
    :members:

User
----

The user model for SilverFlask is already defined and wired up with Flask-Login and Flask-User to provide the whole array of features that you would come to expect from a modern web-application. 

A Permission model is also included to provide fine-grained access control if needed.

FileObject
-----

The file objects reflect the file items uploaded through the CMS. ImageObject is an inherited class which implements common image functionality, such as cropping and resizing.

FileStorageBackend
-----

The `FileStorageBackend` is a class that abstracts away the underlying file storage. At the moment, the only implemented backend is the `LocalFileStorageBackend` which implements methods to save files to the local flask installation (defaults to the `/static/uploads/` folder).

Another FileStorageBackend could, for example, be an implementation for a S3 Backend (e.g. using the boto library).


