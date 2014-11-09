from flask import Blueprint, render_template, flash, request, json, \
    redirect, make_response, url_for, \
    abort
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from silverflask import cache
from silverflask.forms import LoginForm
from silverflask.models import User, SiteTree, Page, SuperPage, \
    FileObject, GalleryImage, SiteConfig
from silverflask.models import DataObject
from silverflask import db
from flask import jsonify
from sqlalchemy import event
from silverflask.models.FileObject import create_file
from flask_user import current_user

from wtforms import Form
from silverflask.models.OrderedForm import OrderedForm

bp = Blueprint('cms', __name__)

@bp.before_request
def restrict_access():
    if not current_user.is_authenticated():
        return redirect(url_for("user.login"))
    elif not current_user.has_roles("admin"):
        return abort(403)


@bp.route("/angular")
def render_ang():
    return render_template("angular.html")

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
    import silverflask.models as models
    _class = getattr(models, page_type)
    page = _class()
    page.content = "Super Düper"
    page.name = "Hammerseite"
    parent_id = request.args.get('parent', None)
    if parent_id:
        page.parent_id = int(parent_id)
    page_form = page.get_cms_form()
    print(page_form)
    page_form = page_form()
    page_form.process(request.form, obj=page)
    if page_form.validate_on_submit():
        page_form.populate_obj(page)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for(".edit_page", page_id=page.id))
    print("ISINSTANCE: %s" % isinstance(page_form, OrderedForm))
    return render_template("page/add.html",
                           page_form=page_form)

@bp.route("/testform")
def testform():
    from silverflask.fields import AsyncFileField, LivingDocsField
    from wtforms.fields import StringField, SubmitField
    form = Form
    form.testfield = StringField("Whatever")
    form.testfield = LivingDocsField("Whatever")
    form.uploadfield = AsyncFileField("test")
    form.submit = SubmitField("submit that fucker")
    return render_template("page/add.html", page_form=form())


@bp.route("/filemanager/delete/<int:file_id>")
def filemanager_delete(self, file_id):
    fo = FileObject.query.get(file_id)
    fo.delete_file_and_self()


@bp.route("/upload", methods=["POST"])
def upload():
    print(request.files)
    import os

    THIS_FOLDER = "silverflask/"
    UPLOAD_FOLDER = "static/uploads/"
    for f in request.files.getlist("file"):
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

        return jsonify(files=[return_dict])
    return "No File uploaded"

@bp.route("/testsort")
def testsort():
    gi = db.session.query(GalleryImage).get(1)
    gi.move_after(4)
    gi = db.session.query(GalleryImage).get(2)
    gi.move_after(0)
    db.session.commit()
    return jsonify(data=[(g.image.url(), g.sort_order) for g in GalleryImage.query.limit(1000)])

@bp.route("/sitetree/sort", methods=["POST"])
def sitetree_sort():
    data = request.get_json()
    if not data:
        abort(403)
    page_id = data["id"]
    page = db.session.query(SiteTree).get(page_id)
    if not page:
        abort(404)
    else:
        page.parent_id = data["new_parent"]
        page.insert_after(data["new_position"], SiteTree)
        db.session.commit()
    return "OK"

class SiteConfigExtension(db.Model):
    __tablename__ = SiteConfig.__tablename__
    __table_args__ = {'extend_existing': True}

    background_color = db.Column(db.String(50))

    def __init__(self, baseclass):
        """overwrite methods of parent class"""
        pass

@bp.route("/deduplicate")
def deduplicate():
    SiteTree.reindex()
    return "Successful?"

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
    form = form(request.form, obj=siteconfig)
    if form.validate_on_submit():
        form.populate_obj(siteconfig)
        db.session.commit()
    return render_template("data_object/edit.html", form=form)
