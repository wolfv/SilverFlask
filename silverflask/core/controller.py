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

    @classmethod
    def create_blueprint(cls, app):
        """
        Method to create a blueprint, derived from a SilverFlask Controller.
        It is one instance per blueprint. TODO: This might be a bad design and
        it should probably better be one instance per request.
        :param app: current app (in flask initialization)
        :return: Blueprint
        """
        inst = cls()
        endpoint = cls.__name__
        url_prefix = cls.url_prefix

        static_folder = 'static'
        static_url_path = '/static'
        if hasattr(cls, 'static_folder'):
            static_folder = cls.static_folder
            static_url_path = '/static'
        print(static_folder)
        blueprint = Blueprint(endpoint, __name__,
                              url_prefix=url_prefix,
                              static_folder=static_folder,
                              static_url_path=static_url_path
                              )
        blueprint.jinja_loader = ThemeTemplateLoader()

        view_funcs = {}
        for url in cls.urls:
            action = cls.urls[url]
            kwargs = {
                'methods': ['GET']
            }
            if action in cls.allowed_actions:
                kwargs['methods'] += ['POST']

            blueprint.add_url_rule(url, cls.urls[url], getattr(inst, cls.urls[url]), **kwargs)

        if hasattr(cls, 'before_request'):
            blueprint.before_request(getattr(inst, 'before_request'))

        template_functions = {}
        for fun in cls.template_functions:
            template_functions[fun] = getattr(inst, inst.template_functions[fun])

        blueprint.context_processor(lambda: template_functions)

        for m in cls.mro():
            if hasattr(m, 'init_blueprint'):
                m.init_blueprint(blueprint)

        return blueprint