from flask import render_template, jsonify, url_for, abort, request, redirect, current_app
from flask_wtf import Form
from flask_user import current_user

from silverflask import db
from silverflask.models import User
from silverflask.fields import GridField
from silverflask.core import Controller
from silverflask.controllers.cms_controller import CMSController

class SecurityController(CMSController):
    url_prefix = CMSController.url_prefix + '/security'
    urls = {
        '/edit/<int:record_id>': 'edit_user',
        '/gridfield': 'get_users',
        '/': 'form'
    }

    allowed_actions = {
        'edit_user'
    }

    @staticmethod
    def edit_user(record_id):
        user_obj = db.session.query(User).get(record_id)
        if not user_obj:
            abort("Not found", 404)
        form_class = User.get_cms_form()
        form = form_class(request.form, obj=user_obj)
        if form.validate_on_submit():
            form.populate_obj(user_obj)
            if form['new_password'].data:
                user_obj.set_password(form['new_password'].data)

            db.session.commit()
            return redirect(url_for(".form"))

        return render_template("data_object/edit.html", elem=user_obj, form=form)

    @staticmethod
    def get_users():
        q = User.query.all()
        res = []
        for r in q:
            d = r.as_dict()
            d.update({"edit_url": url_for(".edit_user", record_id=r.id)})
            res.append(d)
        return jsonify(data=res)

    @staticmethod
    def form():
        class SecurityForm(Form):
            gridfield = GridField(
                urls={"get": url_for(".get_users")},
                buttons=[],
                display_cols=["id", "name"]
            )
        return render_template("assetmanager.html", form=SecurityForm())