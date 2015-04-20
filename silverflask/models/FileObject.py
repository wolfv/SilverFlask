from .DataObject import DataObject
import os
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from silverflask import db
from PIL import Image
import uuid
from flask import current_app, url_for

class FileObject(DataObject, db.Model):
    """
    Contains file information

    :ivar location: Location of the file
    :ivar name: Name of the file (usually filename without extension)
    :ivar type: Contains
    """

    location = db.Column(db.String(250))
    name = db.Column(db.String(250))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'fileobject',
        'polymorphic_on': type
    }

    def __init__(self, file, location=None, folder=None):
        location = current_app.storage_backend.store(file, location)
        print("Saving Location: ", location)
        self.location = location
        self.name = os.path.splitext(location)[0]

    def url(self):
        return current_app.storage_backend.get_url(self.location)

    def delete_file(self):
        current_app.storage_backend.delete(self.location)
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
    __cache_dir__ = "_resized"


    def resize(self, width=None, height=None, mode='crop', background="white"):
        if not height:
            height = width

        def resized_location():
            orig_url = self.location
            (orig_folder, tail) = os.path.split(orig_url)
            (fn, ext) = os.path.splitext(tail)
            cache_path = os.path.join(orig_folder, self.__cache_dir__)
            new_fn = fn + mode + str(width) + str(height) + ext
            full_path = os.path.join(cache_path, new_fn)
            return cache_path, new_fn, full_path

        resized_path, resized_filename, resize_fullpath = resized_location()

        if current_app.storage_backend.exists(resize_fullpath):
            return current_app.storage_backend.get_url(resize_fullpath)
        else:
            fp = current_app.storage_backend.retrieve(self.location)
            unused_var, ext = os.path.splitext(self.location)
            resized_img = self._resize(fp, width, height, mode, background)
            if not resized_img:
                return ""
            tmp_file_path = "/tmp/" + str(uuid.uuid4()) + ext
            resized_img.save(tmp_file_path)
            tmp_file = open(tmp_file_path, "rb")
            current_app.storage_backend.store(tmp_file, resized_path, filename=resized_filename)
            return current_app.storage_backend.get_url(resize_fullpath)

    @staticmethod
    def _resize(filepointer, width=None, height=None, mode=None, background=None):
        print("resizing %r %r %r %r" % (filepointer, width, height, mode))
        try:
            img = Image.open(filepointer)
        except:
            return False
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