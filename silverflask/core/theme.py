# Theming support
# Inspired and partially taken from flask-themes2
import os
import json
import logging

from jinja2.loaders import BaseLoader, FileSystemLoader
from flask import send_from_directory, current_app, url_for
from flask import Blueprint
from werkzeug.utils import cached_property

from silverflask.models import SiteConfig

from flask import _app_ctx_stack as stack

logger = logging.getLogger('silverflask')

class ThemeManager(object):

    def __init__(self, app):
        app.silverflask_theme_manager = self
        themes_path = os.path.join(app.root_path, '..', app.config["SILVERFLASK_THEME_PATH"])
        if os.path.exists(themes_path):
            self.themes = {path: Theme(os.path.join(themes_path, path)) for path in os.listdir(themes_path)}
        else:
            self.themes = {}

    def __getitem__(self, item):
        return self.themes[item]


class ThemeTemplateLoader(BaseLoader):
    """
    This is a template loader that loads templates from the current app's
    loaded themes.
    """

    def __init__(self):
        BaseLoader.__init__(self)

    def get_source(self, environment, template):
        theme = current_app.silverflask_theme_manager[SiteConfig.get_current().theme]
        return theme.jinja_loader.get_source(environment, template)

    def list_templates(self):
        res = []
        fmt = '_themes/%s/%s'
        for ident, theme in current_app.silverflask_theme_manager.themes.items():
            res.extend((fmt % (ident, t))
                       for t in theme.jinja_loader.list_templates())
        return res


def static_file(filename):
    theme = current_app.silverflask_theme_manager[SiteConfig.get_current().theme]
    directory = os.path.join(theme.path, 'static')
    print(directory, filename)
    return send_from_directory(directory, filename)


blueprint = Blueprint("theme", __name__, )
blueprint.jinja_loader = ThemeTemplateLoader()
blueprint.add_url_rule('/theme/<path:filename>', 'static', view_func=static_file)


def global_theme_template(templatename):
    theme = current_app.silverflask_theme_manager[SiteConfig.get_current().theme]
    return os.path.join(theme.folder, 'templates', templatename)


def global_theme_static(filename):
    return url_for('theme.static', filename=filename)


def init_themes(app):
    ThemeManager(app)
    app.jinja_env.globals['theme'] = global_theme_template
    app.jinja_env.globals['theme_static'] = global_theme_static

    app.register_blueprint(blueprint)

class Theme(object):
    """
    This contains a theme's metadata.
    :param path: The path to the theme directory.
    """

    def __init__(self, path):
        #: The theme's root path. All the files in the theme are under this
        #: path.
        self.path = os.path.abspath(path)
        self.relative_path = path
        self.folder = os.path.split(self.path)[1]
        with open(os.path.join(self.path, 'info.json')) as fd:
            self.info = i = json.load(fd)
        try:
            #: The theme's name, as given in info.json. This is the human
            #: readable name.
            self.name = i['name']

            #: The theme's identifier. This is an actual Python identifier,
            #: and in most situations should match the name of the directory the
            #: theme is in.
            self.identifier = i.get('identifier') or os.path.split(self.path)[1]

            #: The human readable description. This is the default (English)
            #: version.
            self.description = i.get('description')

            #: This is a dictionary of localized versions of the description.
            #: The language codes are all lowercase, and the ``en`` key is
            #: preloaded with the base description.
            self.localized_desc = dict(
                (k.split('_', 1)[1].lower(), v) for k, v in i.items()
                if k.startswith('description_')
            )
            self.localized_desc.setdefault('en', self.description)

            #: The author's name, as given in info.json. This may or may not
            #: include their email, so it's best just to display it as-is.
            self.authors = i['authors'] or [i['author']]

            #: A short phrase describing the license, like "GPL", "BSD", "Public
            #: Domain", or "Creative Commons BY-SA 3.0".
            self.license = i.get('license')

            #: A URL pointing to the license text online.
            self.license_url = i.get('license_url')

            #: The URL to the theme's or author's Web site.
            self.website = i.get('website')

            #: The theme's preview image, within the static folder.
            self.preview = i.get('preview')

            #: The theme's version string.
            self.version = i.get('version')

            #: Any additional options. These are entirely application-specific,
            #: and may determine other aspects of the application's behavior.
            self.options = i.get('options', {})
        except KeyError as e:
            logger.warn("Could not load theme {}. The key {} is missing in info.json".format(self.path, e))


    @cached_property
    def static_path(self):
        """
        The absolute path to the theme's static files directory.
        """
        return os.path.join(self.path, 'static')

    @cached_property
    def templates_path(self):
        """
        The absolute path to the theme's templates directory.
        """
        return os.path.join(self.path, 'templates')

    @cached_property
    def license_text(self):
        """
        The contents of the theme's license.txt file, if it exists. This is
        used to display the full license text if necessary. (It is `None` if
        there was not a license.txt.)
        """
        lt_path = os.path.join(self.path, 'license.txt')
        if os.path.exists(lt_path):
            with open(lt_path) as fd:
                return fd.read()
        else:
            return None

    @cached_property
    def jinja_loader(self):
        """
        This is a Jinja2 template loader that loads templates from the theme's
        ``templates`` directory.
        """
        return FileSystemLoader(self.templates_path)