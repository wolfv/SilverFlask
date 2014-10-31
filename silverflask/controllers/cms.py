from flask import Blueprint, render_template, flash, request, json, \
    redirect, make_response, url_for, \
    abort
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from silverflask import cache
from silverflask.forms import LoginForm
from silverflask.models import db, User, SiteTree, Page, SuperPage, FileObject
from flask import jsonify

from wtforms import Form

bp = Blueprint('cms', __name__)

@bp.route("/get_sitetree")
def get_sitetree():
    s = SiteTree.get_sitetree()
    resp = make_response(json.dumps(s), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp
    return jsonify(data=s)

@bp.route("/")
def main():
    sitetree = SiteTree.get_sitetree()
    print(sitetree)
    return render_template("cms.html")


@bp.route("/testedit", methods=["GET", "POST"])
def testedit():
    page = SiteTree.query.get_or_404(1)
    page.urlsegment = "drolf"
    db.session.commit()
    db.session.flush()


@bp.route("/edit/page/<int:page_id>", methods=["GET", "POST"])
def edit_page(page_id):
    page = db.session.query(SiteTree).get(page_id)
    if not page:
        abort(404)
    page_form = page.get_cms_form()
    page_form = page_form(request.form, obj=page)
    if page_form.validate_on_submit():
        page_form.populate_obj(page)
        db.session.commit()

    return render_template("edit_page.html",
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
    page_form = page_form(request.form, obj=page)
    if page_form.validate_on_submit():
        page_form.populate_obj(page)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("admin.main"))
    return render_template("add_page.html",
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
    return render_template("add_page.html", page_form=form())

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
        # filename = f.filename
        # url = os.path.join(UPLOAD_FOLDER, filename)
        # f.save(os.path.join(THIS_FOLDER, url))
        fo = FileObject(f)
        db.session.add(fo)
        db.session.commit()

        return_dict = {
            "name": fo.name,
            "url": fo.url(),
            "thumbnailUrl": "",
            "deleteUrl": url_for(".filemanager_delete", file_id=fo.id),
            "deleteType": "DELETE"
        }

        return jsonify(files=[return_dict])
    return "No File uploaded"
