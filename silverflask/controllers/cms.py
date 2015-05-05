from os import listdir
from flask import Blueprint, render_template, flash, request, json, \
    redirect, make_response, url_for, \
    abort, session, current_app, send_from_directory
from silverflask.models import User, SiteTree, Page, SuperPage, \
    FileObject, GalleryImage, SiteConfig
from silverflask import db
from flask import jsonify
from flask_user import current_user
from silverflask.models.FileObject import create_file
from silverflask.models.OrderedForm import OrderedFormFactory

bp = Blueprint('cms', __name__)

@bp.context_processor
def pagetypes():
    return dict(pagetypes=SiteTree.pagetypes())

@bp.before_request
def restrict_access():
    current_app.logger.debug("Restricting access: %s" % str(current_user.is_authenticated()))
    if not current_user.is_authenticated():
        return redirect(url_for("user.login", next=request.url))
    elif not current_user.has_roles("admin"):
        current_app.logger.debug("%s, %s" % (current_user.has_roles("admin"), str(current_user.roles)))
        return abort(403)


@bp.route("/get_sitetree")
def get_sitetree():
    s = SiteTree.get_sitetree()
    resp = make_response(json.dumps(s), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
    return jsonify(data=s)


@bp.route("/add_gallery")
def add_gallery():
    gi = GalleryImage()
    gi.image = FileObject.query.get(1)
    db.session.add(gi)
    db.session.commit()
    return jsonify(data=[(g.image.url(), g.sort_order)for g in GalleryImage.query.limit(1000)])


@bp.route("/")
def main():
    return redirect(url_for(".pages"))

@bp.route("/pages")
def pages():
    return render_template("page/index.html")

@bp.route("/edit/page/<int:page_id>", methods=["GET", "POST"])
def edit_page(page_id):
    page = db.session.query(SiteTree).get(page_id)
    if not page:
        abort(404)
    page_form = page.get_cms_form()
    if type(page_form) == OrderedFormFactory:
        page_form = page_form.create()

    page_form = page_form(request.form, obj=page)

    if page_form.validate_on_submit():
        page_form.populate_obj(page)
        if request.form.get("Publish"):
            page.mark_as_published()

        db.session.commit()
    return render_template("page/edit.html",
                           page=page,
                           page_form=page_form)

@bp.route("/add_page/<page_type>", methods=["GET", "POST"])
def add_page(page_type):
    import silverflask.models.models as models
    _class = getattr(models, page_type)
    page = _class()
    page.content = "Super Düper"
    page.name = "Hammerseite"
    parent_id = request.args.get('parent', None)
    if parent_id:
        page.parent_id = int(parent_id)
    page_form = page.get_cms_form()

    if type(page_form) == OrderedFormFactory:
        page_form = page_form.create()

    page_form = page_form()
    page_form.process(request.form, obj=page)
    if page_form.validate_on_submit():
        page_form.populate_obj(page)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for(".edit_page", page_id=page.id))


    return render_template("page/add.html",
                           page_form=page_form)


@bp.route("/filemanager/delete/<int:file_id>")
def filemanager_delete(self, file_id):
    fo = FileObject.query.get(file_id)
    fo.delete_file_and_self()


@bp.route("/upload", methods=["POST"])
def upload():
    print(request.files)
    files = request.files
    if len(request.files.getlist("files[]")):
        files = request.files.getlist("files[]")
    def _create_file(f):
        fo = create_file(f)
        db.session.add(fo)
        db.session.commit()
        return_dict = {
            "id": fo.id,
            "name": fo.name,
            "url": fo.url(),
            "thumbnailUrl": "",
            "deleteUrl": url_for(".filemanager_delete", file_id=fo.id),
            "deleteType": "DELETE"
        }
        return return_dict
    res = []
    if type(files) == list:
        for f in files:
            res.append(_create_file(f))
    else:
        for k in files:
            res.append(_create_file(files[k]))

    if len(res):
        return jsonify(files=res)
    else:
        abort(403, "No Files Uploaded")


@bp.route("/sitetree/sort", methods=["POST"])
def sitetree_sort():
    data = request.get_json()
    if not data:
        abort(403, 'No JSON data sent!')
    page_id = data["id"]
    page = db.session.query(SiteTree).get(page_id)
    if not page:
        abort(404, 'Page not found!')
    else:
        try:
            page.set_parent(data["new_parent"])
        except Exception as e:
            db.session.rollback()
            abort(500, str(e))
        page.insert_after(int(data["new_position"]), SiteTree,
                          query=SiteTree.query.filter(SiteTree.parent_id == data["new_parent"]),
                          index_absolute=False)
        print(page.sort_order)
        db.session.commit()
    return jsonify(message='Successfully sorted page tree', type="success")

class SiteConfigExtension(db.Model):
    __tablename__ = SiteConfig.__tablename__
    __table_args__ = {'extend_existing': True}

    background_color = db.Column(db.String(50))

    def __init__(self, baseclass):
        """overwrite methods of parent class"""
        pass

# @bp.route("/deduplicate")
# def deduplicate():
#     SiteTree.reindex()
#     return "Successful?"


@bp.route("/siteconfig", methods=["POST", "GET"])
def edit_siteconfig():
    # In the current configuration there is only one SiteConfig
    # This would change if more "Sites" are configured through one CMS
    siteconfig = db.session.query(SiteConfig).first()
    if not siteconfig:
        siteconfig = SiteConfig()
        db.session.add(siteconfig)
        db.session.commit()

    form = siteconfig.get_cms_form()
    # form.fields['theme'].choices = get_available_themes()
    form = form(request.form, obj=siteconfig)
    if form.validate_on_submit():
        form.populate_obj(siteconfig)
        db.session.commit()
    return render_template("data_object/edit.html", form=form)

@bp.route("/draft/activate")
@bp.route("/draft/activate/<int:page_id>")
def activate_draft(page_id=None):
    session["draft"] = True
    if page_id:
        page = db.session.query(SiteTree).get(page_id)
        if page:
            redirect_url = page.get_url()
            return redirect(redirect_url)
    return redirect("/")

@bp.route("/draft/deactivate")
@bp.route("/draft/deactivate/<int:page_id>")
def deactivate_draft(page_id=None):
    session["draft"] = False
    if page_id:
        page = db.session.query(SiteTree.LiveType).get(page_id)
        if page:
            redirect_url = page.get_url()
            return redirect(redirect_url)
    return redirect("/")
