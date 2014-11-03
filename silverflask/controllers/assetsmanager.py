from .cms import bp
from silverflask.models import FileObject
from flask_wtf import Form
from flask import render_template, jsonify, url_for
from silverflask.fields import GridField
from silverflask import db


@bp.route("/assets/gridfield")
def assets_get():
    q = FileObject.query.all()
    return jsonify(data=[r.as_dict() for r in q])


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

