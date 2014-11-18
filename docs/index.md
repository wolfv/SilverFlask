# SilverFlask

SilverFlask aims to be the first full-featured CMS building on top of solid foundations such as Flask, SQLAlchemy, Jinja2 and a huge number of plugins built on top of these such as SQLAlchemy-continuum, Flask-User, Flask Login and countless others.

SilverFlask aims to create an environment that is exceptionally friendly for newbies and experienced developers alike.

SilverFlask is partly named after SilverStripe, one of the best and fully-featured CMS's around in PHP land. However, for my taste it had a few shortcomings. Of course, PHP as a programming language is multitudes less pleasant than python. And unfortunately, SilverStripe is built around a framework that is more or less made only for the CMS. I personally don't like this tight coupling as the framework has not gotten much exposure outside of the SilverStripe CMS world.
On the other hand, Flask is a very mature framework, and python is a lovely programming language.

## The basic building blocks

SilverFlask defines a number of basic building blocks for websites.

### DataObject

The DataObject is the most basic building block of any CMS model. The 

### SiteTree

The SiteTree is the database model from which all pages have to inherit. It defines the parent/children relationships of the page tree. It also defines everything that's needed to get nice URL slugs working. 

### User

The user model for SilverFlask is already defined and wired up with Flask-Login and Flask-User to provide the whole array of features that you would come to expect from a modern web-application. 

A Permission model is also included to provide fine-grained access control if needed.

### FileObject

The file objects reflect the file items uploaded through the CMS. ImageObject is an inherited class which implements common image functionality, such as cropping and resizing.

#### FileStorageBackend

The `FileStorageBackend` is a class that abstracts away the underlying file storage. At the moment, the only implemented backend is the `LocalFileStorageBackend` which implements methods to save files to the local flask installation (defaults to the `/static/uploads/` folder).

Another FileStorageBackend could, for example, be an implementation for a S3 Backend (e.g. using the boto library).


