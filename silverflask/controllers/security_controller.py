from flask import render_template, jsonify, url_for, abort, request, redirect, current_app
from flask_wtf import Form
from flask_user import current_user

from silverflask import db
from silverflask.models import User
from silverflask.fields import GridField
from silverflask.core import Controller


class AdminController(Controller):
    url_prefix = '/admin'
    before_request = 'check_authorization'

    @staticmethod
    def check_authorization():
        current_app.logger.debug("Restricting access: %s" % str(current_user.is_authenticated()))
        if not current_user.is_authenticated():
            return redirect(url_for("user.login", next=request.url))
        elif not current_user.has_roles("admin"):
            current_app.logger.debug("%s, %s" % (current_user.has_roles("admin"), str(current_user.roles)))
            return abort(403)


class SecurityController(AdminController):
    url_prefix = AdminController.url_prefix + '/security'
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