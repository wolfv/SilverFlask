from flask import Blueprint, render_template, abort, session, current_app, request
from silverflask.models import User, SiteTree, ErrorPage, SiteConfig
from flask import send_from_directory
from flask import current_app, app, url_for
import flask

main = Blueprint('main', __name__)

def setup_processors(app):

    @app.context_processor
    def hierarchy():
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

        def level(num):
            current_page = cls.get_by_url(request.path)
            level = 0
            while current_page.parent:
                level += 1
                current_page = current_page.parent
            if level != num:
                return False

        return dict(menu=menu, level=level)

    @app.context_processor
    def get_siteconfig():
        siteconfig = SiteConfig.query.first()
        return dict(siteconfig=siteconfig)

    @app.context_processor
    def utilities():
        def themed_css(arg):
            return url_for('theme.static', filename="css/" + arg)

        def themed_js(arg):
            return url_for('theme.static', filename="js/" + arg)

        return {
            'themed_css': themed_css,
            'themed_js': themed_js
        }
        # main.static_folder

@main.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(current_app.config['SILVERFLASK_ABSOLUTE_UPLOAD_PATH'],
                               filename)

@main.errorhandler(404)
def page_not_found(e):
    print(e)
    try:
        error_page = ErrorPage.query.filter(ErrorPage.error_code == 404).one()
        return render_template(error_page.template, error_page)
    except:
        # No error page ...
        return "Sorry!", 404

def init_blueprint(app):
    main.template_folder = app.root_path + "/../themes"
    main.static_folder = app.root_path + "/../themes"
    return main
