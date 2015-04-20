from flask import Blueprint, render_template, abort, session, current_app
from silverflask.models import User, SiteTree
from silverflask.models import SiteConfig
from flask import send_from_directory

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
@main.route('/<path:url_segment>')
def silverflask_page(url_segment=None):
    if not url_segment:
        url_segment = current_app.config["HOME_URLSEGMENT"]
    if session.get("draft"):
        page = SiteTree.get_by_url(url_segment)
    else:
        page = SiteTree.get_by_url(url_segment, SiteTree.LiveType)
    if not page:
        return abort(404, "Page not found")

    template = page.template
    return render_template(template, page=page, **page.as_dict())


@main.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(current_app.config['SILVERFLASK_ABSOLUTE_UPLOAD_PATH'],
                               filename)
