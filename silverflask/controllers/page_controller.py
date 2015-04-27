from flask import Blueprint, request, render_template
from silverflask.models import SiteTree
class Controller(object):

    urlprefix = None
    route_base = '/'
    urls = {
        'controller': 'index'
    }

    def index(self):
        return "Top sache"

    def create_blueprint(self):
        self.endpoint = self.__class__.__name__
        urlprefix = self.urlprefix or self.__class__.__name__

        self.blueprint = Blueprint(self.endpoint, __name__,
                                   url_prefix=self.route_base)
        for url in self.urls:
            self.blueprint.add_url_rule(url, self.urls[url], getattr(self, self.urls[url]))

        return self.blueprint


class SiteTreeController(Controller):

    urls = {
        'sitetree/<path:url_segment>': 'index'
    }

    def index(self, url_segment):
        page = SiteTree.get_by_url(url_segment)
        print(page, page.children, page.parent)
        return render_template(page.template, page=page, **page.as_dict())


