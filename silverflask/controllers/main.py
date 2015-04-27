from flask import Blueprint, render_template, abort, session, current_app, request
from silverflask.models import User, SiteTree
from silverflask.models import SiteConfig
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
            return url_for('main.serve_theme_file', filename="css/" + arg)

        def themed_js(arg):
            return url_for('main.serve_theme_file', filename="js/" + arg)

        return {
            'themed_css': themed_css,
            'themed_js': themed_js
        }
        # main.static_folder

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
    theme = SiteConfig.get_current().theme
    template_path = theme + '/templates/' + template
    return render_template(template_path, page=page, **page.as_dict())


@main.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(current_app.config['SILVERFLASK_ABSOLUTE_UPLOAD_PATH'],
                               filename)

@main.route('/theme/<path:filename>')
def serve_theme_file(filename):
    theme = SiteConfig.get_current().theme
    filename = theme + '/' + filename
    return send_from_directory(main.template_folder,
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
