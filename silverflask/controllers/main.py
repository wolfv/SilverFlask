from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_user import login_required
from silverflask import cache, db
from silverflask.forms import LoginForm
from silverflask.models import User, SiteTree
from flask import jsonify
from silverflask.models import SiteConfig
from flask_user import current_user

from .. import app

main = Blueprint('main', __name__)

@app.context_processor
def get_menu():
    print("IS THAT A DRAFT?")
    if request.args.get("draft"):
        print("DRAFT MENU")
        cls = SiteTree
    else:
        cls = SiteTree.LiveType
    def menu(parent=None):
        if parent == 0:
            parent = None
        print("Getting Menu for parent: %r" % parent)
        return [r for r in
                cls.query.filter(cls.parent_id == parent)]
    return dict(menu=menu)


@app.context_processor
def get_siteconfig():
    siteconfig = SiteConfig.query.first()
    return dict(siteconfig=siteconfig)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # For demonstration purposes the password in stored insecurely
        user = User.query.filter_by(username=form.username.data,
                                    password=form.password.data).first()

        if user:
            login_user(user)

            flash("Logged in successfully.", "success")
            return redirect(request.args.get("next") or url_for(".home"))
        else:
            flash("Login failed.", "danger")

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200

@main.route("/data")
def data():
    ss = SiteTree.query.limit(100)
    data = [s.as_dict() for s in ss]
    return jsonify(data=data)


@main.route('/<path:urlsegment>')
def get_page(urlsegment):
    if request.args.get("draft") and (current_user.is_authenticated() and current_user.has_roles("admin")):
        page = SiteTree.get_by_url(urlsegment)
    else:
        page = SiteTree.get_by_url(urlsegment, SiteTree.LiveType)
    if not page:
        return "Not found", 404
    return render_template('page.html', **page.as_dict())
