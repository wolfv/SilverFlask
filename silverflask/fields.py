from wtforms.fields import FileField, TextAreaField
from wtforms.widgets.core import HTMLString, html_params

class AsyncFileUpload(object):
    """
    Renders a file input chooser field.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return HTMLString("""<div id="filelist">Your browser doesn't have Flash, Silverlight or HTML5 support.</div>
<br />

<div id="container">
    <a id="pickfiles" href="javascript:;">[Select files]</a>
    <a id="uploadfiles" href="javascript:;">[Upload files]</a>
</div>
<div id="console"></div>

""")

class LivingDocsWidget(object):
    def __call__(self, *args, **kwargs):
        return HTMLString("""<div class="doc-toolbar"></div><div class="editor-section"></div>""")

class AsyncFileField(FileField):
    widget = AsyncFileUpload()

class LivingDocsField(TextAreaField):
    widget = LivingDocsWidget()