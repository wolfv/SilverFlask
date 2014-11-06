from .DataObject import DataObject
import os
from werkzeug.datastructures import FileStorage
from wtforms import fields
from silverflask import db
from PIL import Image
import uuid
import errno
import shutil

class FileStorageBackend(object):
    def store(self, filepointer, location):
        raise NotImplementedError()

    def exists(self, location):
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

    def get_store_path(self, location):
        path_tmp = os.path.join(self.upload_folder, location)
        return './silverflask' + path_tmp


    def store(self, read_pointer, location):
        path = self.get_store_path(location)
        try:
            folder_path = os.path.dirname(path)
            os.makedirs(folder_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if isinstance(read_pointer, FileStorage):
            read_pointer.save(path)
            return self.get_url(location)

        write_pointer = open(path, 'wb')
        print(path)
        shutil.copyfileobj(read_pointer, write_pointer)
        return self.get_url(location)

    def exists(self, path):
        return os.path.exists(path)

    def retrieve(self, location):
        path = self.get_store_path(location)
        if not self.exists(path):
            return None
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
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'fileobject',
        'polymorphic_on': type
    }

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

    @classmethod
    def get_cms_form(cls):
        form = super().get_cms_form()
        # form.location = fields.FileField("File")
        return form


    def as_dict(self):
        d = super().as_dict()
        d.update({
            "id": self.id,
            "name": self.name,
            "location": self.location
        })
        return d


class ImageObject(FileObject):

    __tablename__ = "imageobject"
    __mapper_args__ = {
        'polymorphic_identity': __tablename__
    }

    # Specifies special operations on Image Files
    id = db.Column(db.Integer, db.ForeignKey('fileobject.id'), primary_key=True)
    __cache_dir__ = "/_resized/"


    def resize(self, width=None, height=None, mode='crop', background="white"):
        if not height:
            height = width

        def resized_location():
            orig_url = storage_backend.get_url(self.location)
            (orig_folder, tail) = os.path.split(orig_url)
            (fn, ext) = os.path.splitext(tail)
            new_fn = fn + mode + str(width) + str(height) + ext
            return orig_folder + self.__cache_dir__ + new_fn
        rl = resized_location()
        if storage_backend.exists(rl):
            return rl
        else:
            fp = storage_backend.retrieve(self.location)
            unused_var, ext = os.path.splitext(self.location)
            resized_img = self._resize(fp, width, height, mode, background)
            tmp_file_path = "/tmp/" + str(uuid.uuid4()) + ext
            resized_img.save(tmp_file_path)
            tmp_file = open(tmp_file_path, "rb")
            print("STORING RESIZED IMAGE")
            storage_backend.store(tmp_file, rl)
            return rl

    @staticmethod
    def _resize(filepointer, width=None, height=None, mode=None, background=None):
        print("resizing %r %r %r %r" % (filepointer, width, height, mode))
        img = Image.open(filepointer)
        orig_width, orig_height = img.size

        width = min(width, orig_width) if width else None
        height = min(height, orig_height) if height else None

        if not img.mode.lower().startswith('rgb'):
            img = img.convert('RGBA')

        if width and height:

            fit, crop = sorted([
                (width, orig_height * width // orig_width),
                (orig_width * height // orig_height, height)
            ])

            if mode == 'fit' or mode == 'pad':
                img = img.resize(fit, Image.ANTIALIAS)

                if mode == 'pad':
                    pad_color = str(background or 'black')
                    back = Image.new('RGBA', (width, height), pad_color)
                    back.paste(img, (
                        (width - fit[0]) // 2,
                        (height - fit[1]) // 2
                    ))
                    img = back

            elif mode == 'crop':
                dx = (crop[0] - width) // 2
                dy = (crop[1] - height) // 2
                img = img.resize(crop, Image.ANTIALIAS).crop(
                    (dx, dy, dx + width, dy + height)
                )

            elif mode == 'reshape' or mode is None:
                img = img.resize((width, height), Image.ANTIALIAS)

            else:
                raise ValueError('unsupported mode %r' % mode)

        elif width:
            height = orig_height * width // orig_width
            img = img.resize((width, height), Image.ANTIALIAS)

        elif height:
            width = orig_width * height // orig_height
            img = img.resize((width, height), Image.ANTIALIAS)

        return img

def create_file(f):
    import mimetypes
    mime = mimetypes.guess_type(f.filename)
    if mime[0].startswith("image"):
        return ImageObject(f)
    else:
        return FileObject(f)