from .cms import bp
from silverflask.models import FileObject
from flask_wtf import Form
from flask import render_template, jsonify
from silverflask.fields import GridField

@bp.route("/assets")
def assets():
    q = FileObject.query.limit(100)
    assets_form = Form
    assets_form.gridfield = GridField("test")
    print(assets_form.gridfield)
    return render_template("assetmanager.html", page_form=assets_form())
    for f in q:
        print(f.as_dict())
    return str([f.as_dict for f in q])

@bp.route("/gridfield/<id>")
def gridfield_response(id):
    q = FileObject.query.limit(100)
    return jsonify(data=[f.as_dict() for f in q])
