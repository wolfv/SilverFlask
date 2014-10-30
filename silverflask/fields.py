from wtforms.fields import FileField, TextAreaField
from wtforms.widgets.core import HTMLString, html_params
from flask import render_template


class AsyncFileUpload(object):
    """
    Renders a file input chooser field.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return render_template("forms/AsyncFileUploadWidget.html")


class LivingDocsWidget(object):
    def __call__(self, field, **kwargs):
        print(kwargs)
        print(field._value())
        return render_template("forms/LivingDocsWidget.html",
                               field_name=field.id,
                               value=field._value(),
                               **kwargs)


class AsyncFileField(FileField):
    widget = AsyncFileUpload()


class LivingDocsField(TextAreaField):
    widget = LivingDocsWidget()