import os
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
import errno
import shutil
from flask import current_app, url_for
import re

class FileStorageBackend(object):
    """
    The file storage backend abstracts away different file storage providers.

    """
    def store(self, filepointer, location):
        """
        Store a file in a given location

        :param filepointer: filepointer which can be read
        :param location: location where the file should be put, should be a string with slashes indicating folders
        :return: url of stored file
        """
        raise NotImplementedError()

    def exists(self, location):
        """
        Check if file exists at given location (i.e. for overwrite checking)

        :param location: string with slash delimited location data (i.e. /folder/file.png)
        :return: boolean True if file exists
        """
        raise NotImplementedError()

    def retrieve(self, location):
        """
        Returns file pointer to file

        :param location: string with slash delimited location data (i.e. /folder/file.png)
        :return: filepointer to file at location or Null
        """
        raise NotImplementedError()

    def delete(self, location):
        """
        Deletes file from storage

        :param location: string with slash delimited location data (i.e. /folder/file.png)
        :return: True if successful, otherwise raises error
        """
        raise NotImplementedError()

    def get_url(self, location):
        """
        Return public url for file

        :param location: string with slash delimited location data (i.e. /folder/file.png)
        :return:
        """
        raise NotImplementedError()


class LocalFileStorageBackend(FileStorageBackend):
    """
    Currently the only implemented storage backend. Stores files in ``/static/uploads/`` folder in your flask
    application folder
    """
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def get_upload_path(self, filename, location=None):
        filename = secure_filename(filename)
        if location:
            location = re.sub('[^\w\- ]', '_', location)
            location = location.lstrip('/').rstrip('/')
        else:
            return filename
        return os.path.join(location, filename)

    def get_store_path(self, filename, location=None):
        return os.path.join(self.upload_folder,
                            self.get_upload_path(filename, location))

    def store(self, read_pointer, path, filename=None):
        if not filename and isinstance(read_pointer, FileStorage):
            filename = read_pointer.filename
        elif not filename:
            filename = read_pointer.name
        absolute_path = self.get_store_path(filename, path)
        try:
            folder_path = os.path.dirname(absolute_path)
            os.makedirs(folder_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                pass

        if isinstance(read_pointer, FileStorage):
            read_pointer.save(absolute_path)
            return self.get_upload_path(filename, path)

        write_pointer = open(absolute_path, 'wb+')
        shutil.copyfileobj(read_pointer, write_pointer)
        return self.get_upload_path(filename, path)

    def exists(self, path):
        store_path = self.get_store_path(path)
        if os.path.exists(store_path):
            return store_path
        else:
            return None

    def retrieve(self, location):
        exists = self.exists(location)
        if not exists:
            return None
        read_pointer = open(exists, 'rb')
        return read_pointer

    def delete(self, location):
        if os.path.exists(location):
            os.remove(location)

    def get_url(self, location):
        print("GeTTING URL: ", location)
        return url_for('main.serve_file', filename=location)
        # return url_for('static', 'uploads/' + location)
