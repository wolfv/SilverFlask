from .cms import bp
from silverflask.models import User
from flask_wtf import Form
from flask import render_template, jsonify, url_for, abort, request, redirect
from silverflask.fields import GridField
from silverflask import db

@bp.route("/security/edit/<int:record_id>", methods=["POST", "GET"])
def user_edit(record_id):
    user_obj = db.session.query(User).get(record_id)
    if not user_obj:
        abort("Not found", 404)
    form_class = User.get_cms_form()
    form = form_class(request.form, obj=user_obj)
    if form.validate_on_submit():
        form.populate_obj(user_obj)
        if form.new_password.data:
            user_obj.set_password(form.new_password.data)

        db.session.commit()
        return redirect(url_for(".securitymanager"))

    return render_template("data_object/edit.html", elem=user_obj, form=form)

@bp.route("/security/gridfield")
def user_get():
    q = User.query.all()
    res = []
    for r in q:
        d = r.as_dict()
        d.update({"edit_url": url_for(".user_edit", record_id=r.id)})
        res.append(d)
    return jsonify(data=res)


@bp.route("/security")
def securitymanager():
    class SecurityForm(Form):
        gridfield = GridField(
            urls={"get": url_for(".user_get")},
            buttons=[],
            display_rows=["id", "name"]
        )
    return render_template("assetmanager.html", form=SecurityForm())

