from flask import request, render_template, session, current_app, abort
from silverflask.models import SiteTree, SiteConfig
from silverflask.core import Controller, render_themed

class SiteTreeController(Controller):

    urls = {
        '/': 'index',
        '/<path:url_segment>': 'index'
    }

    template_functions = {
        'menu': 'menu',
        'level': 'level',
        'bread_crumbs': 'bread_crumbs',
        'linking_mode': 'linking_mode'
    }

    @staticmethod
    def class_from_session():
        if session.get("draft"):
            cls = SiteTree
        else:
            cls = SiteTree.LiveType
        return cls

    @staticmethod
    def level(num):
        cls = SiteTreeController.class_from_session()
        current_page = cls.get_by_url(request.path)
        level = 0
        while current_page.parent:
            level += 1
            current_page = current_page.parent
        if level != num:
            return False

    @staticmethod
    def bread_crumbs(num):
        cls = SiteTreeController.class_from_session()
        current_page = cls.get_by_url(request.path)
        level = 0
        while current_page.parent:
            level += 1
            current_page = current_page.parent
        if level != num:
            return False

    @staticmethod
    def menu(parent=None):
        cls = SiteTreeController.class_from_session()
        if parent == 0:
            parent = None
        print("Getting Menu for parent: %r" % parent)
        return [r for r in
                cls.query.filter(cls.parent_id == parent).all()]

    def linking_mode(self, page):
        cls = SiteTreeController.class_from_session()
        if page.id == self.current_page.id:
            return "current"

        if page in self.current_page.parents():
            return "section"
        return "link"

    def index(self, url_segment=None):
        if not url_segment:
            url_segment = current_app.config["SILVERFLASK_HOME_URLSEGMENT"]
        if session.get("draft"):
            page = SiteTree.get_by_url(url_segment)
        else:
            page = SiteTree.get_by_url(url_segment, SiteTree.LiveType)
        if not page:
            return abort(404, "Page not found")

        self.current_page = page
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                print(rule, rule.endpoint)

        template = page.template


        return render_themed(template, page=page, **page.as_dict())


