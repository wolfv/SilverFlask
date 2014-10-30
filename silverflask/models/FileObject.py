from .DataObject import DataObject
import os

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class FileObject(DataObject, db.Model):
    location = db.Column(db.String(250))
    name = db.Column(db.String(250))

    def __init__(self, location):
        self.location = location
        self.name = os.path.splitext(location)[0]

    def url(self):
        return "/" + self.location

    def delete_file(self):
        os.remove(self.location)
        self.location = ""
        self.name = "DELETED"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location
        }