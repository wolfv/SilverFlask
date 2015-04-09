from flask import Blueprint, render_template, abort, session, current_app
from flask_user import login_required
from silverflask import cache, db
from silverflask.forms import LoginForm
from silverflask.models import User, SiteTree
from flask import jsonify
from silverflask.models import SiteConfig
from flask_user import current_user

main = Blueprint('main', __name__)

def setup_processors(app):

    @app.context_processor
    def get_menu():
        if session.get("draft"):
            cls = SiteTree
        else:
            cls = SiteTree.LiveType
        def menu(parent=None):
            if parent == 0:
                parent = None
            print("Getting Menu for parent: %r" % parent)
            return [r for r in
                    cls.query.filter(cls.parent_id == parent).all()]
        return dict(menu=menu)


    @app.context_processor
    def get_siteconfig():
        siteconfig = SiteConfig.query.first()
        return dict(siteconfig=siteconfig)


@main.route('/')
def home():
    page = SiteTree.query.filter(
        SiteTree.parent_id == None,
        SiteTree.urlsegment == current_app.config["HOME_URLSEGMENT"]).scalar()
    if not page:
        page = SiteTree.query.first()
    if not page:
        abort(404)
    return render_template(page.template, page=page, **page.as_dict()   )


@main.route('/<path:urlsegment>')
def get_page(urlsegment):
    print("Getting Page \n\n\n\n")
    if session.get("draft"):
        page = SiteTree.get_by_url(urlsegment)
    else:
        page = SiteTree.get_by_url(urlsegment, SiteTree.LiveType)
    if not page:
        return "Not found", 404
    template = page.template
    print(page.as_dict())
    return render_template(template, page=page, **page.as_dict())
