from .DataObject import DataObject
import os
from werkzeug.datastructures import FileStorage

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class FileStorageBackend(object):
    def store(self, filepointer, location):
        raise NotImplementedError()

    def retrieve(self, location):
        raise NotImplementedError()

    def delete(self, location):
        raise NotImplementedError()

    def get_url(self, location):
        raise NotImplementedError()

class LocalFileStorageBackend(FileStorageBackend):
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.program_folder = "./silverflask"

    def store(self, read_pointer, location):
        path_tmp = os.path.join(self.upload_folder, location)
        path = './silverflask' + path_tmp
        if isinstance(read_pointer, FileStorage):
            read_pointer.save(path)
            return self.get_url(location)

        write_pointer = open(path)
        write_pointer.write(read_pointer.read())
        write_pointer.close()
        return self.get_url(location)

    def retrieve(self, location):
        path = os.path.join(self.upload_folder, location)
        read_pointer = open(path, 'rb')
        return read_pointer

    def delete(self, location):
        if os.path.exists(location):
            os.remove(location)

    def get_url(self, location):
        return self.upload_folder + location
        # return url_for('static', 'uploads/' + location)

storage_backend = LocalFileStorageBackend("/static/uploads/")

class FileObject(DataObject, db.Model):
    location = db.Column(db.String(250))
    name = db.Column(db.String(250))

    def __init__(self, file, location=None):
        if not location and isinstance(file, FileStorage):
            location = file.filename
        storage_backend.store(file, location)
        self.location = location
        self.name = os.path.splitext(location)[0]

    def url(self):
        return storage_backend.get_url(self.location)

    def delete_file(self):
        storage_backend.delete(self.location)
        self.location = ""
        self.name = "DELETED"

    def as_dict(self):
        d = super().as_dict()
        d.update({
            "id": self.id,
            "name": self.name,
            "location": self.location
        })
        return d