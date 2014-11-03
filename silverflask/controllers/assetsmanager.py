from .cms import bp
from silverflask.models import FileObject
from flask_wtf import Form
from flask import render_template, jsonify, url_for, abort, request
from silverflask.fields import GridField
from silverflask import db

url_prefix = "/assets"

@bp.route("/assets/edit/<int:record_id>", methods=["POST", "GET"])
def assets_edit(record_id):
    f = db.session.query(FileObject).get(record_id)
    if not f:
        abort("Not found", 404)
    form_class = FileObject.get_cms_form()
    form = form_class(request.form, obj=f)
    if form.validate_on_submit():
        form.populate_obj(f)
        db.session.commit()
        return "Succeeded"

    return render_template("assetmanager/edit.html", elem=f, page_form=form)

@bp.route("/assets/gridfield")
def assets_get():
    q = FileObject.query.all()
    res = []
    for r in q:
        d = r.as_dict()
        d.update({"edit_url": url_for(".assets_edit", record_id=r.id)})
        res.append(d)
    return jsonify(data=res)


@bp.route("/assets")
def assets():
    q = FileObject.query.limit(100)
    assets_form = Form
    assets_form.gridfield = GridField(
        urls={"get": url_for(".assets_get")},
        buttons=[],
        display_rows=["id", "name"]
    )
    print(assets_form.gridfield)
    return render_template("assetmanager.html", page_form=assets_form())

