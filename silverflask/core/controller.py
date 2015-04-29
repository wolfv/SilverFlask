# The main implementation of a Flask controller
# that gives a blueprint
from flask import Blueprint
from silverflask.core.theme import ThemeTemplateLoader

class Controller(object):

    url_prefix = ''
    urls = {
        '/': 'index'
    }
    allowed_actions = {}
    template_functions = {
        'linking_mode': 'linking_mode'
    }

    @staticmethod
    def linking_mode():
        return ''

    def create_blueprint(self, app):
        self.endpoint = self.__class__.__name__
        url_prefix = self.url_prefix

        self.blueprint = Blueprint(self.endpoint, __name__,
                                   url_prefix=url_prefix)
        self.blueprint.jinja_loader = ThemeTemplateLoader()

        for url in self.urls:
            action = self.urls[url]
            kwargs = {
                'methods': ['GET']
            }
            if action in self.allowed_actions:
                kwargs['methods'] += ['POST']

            self.blueprint.add_url_rule(url, self.urls[url], getattr(self, self.urls[url]), **kwargs)

        if hasattr(self, 'before_request'):
            self.blueprint.before_request(getattr(self, self.before_request))

        template_functions = {}
        for fun in self.template_functions:
            template_functions[fun] = getattr(self, self.template_functions[fun])

        self.blueprint.context_processor(lambda: template_functions)

        for m in self.__class__.mro():
            if hasattr(m, 'init_blueprint'):
                m.init_blueprint(self.blueprint)

        return self.blueprint
