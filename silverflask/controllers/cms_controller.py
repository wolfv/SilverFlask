from flask import current_app, make_response, redirect, url_for, abort,\
    request, session, json
from flask_user import current_user

from silverflask import db
from silverflask.models import SiteTree
from silverflask.core import Controller, render_template


class CMSController(Controller):

    def before_request(self):
        current_app.logger.debug("Restricting access: %s" % str(current_user.is_authenticated()))
        if not current_user.is_authenticated():
            return redirect(url_for("user.login", next=request.url))
        elif not current_user.has_roles("admin"):
            current_app.logger.debug("%s, %s" % (current_user.has_roles("admin"), str(current_user.roles)))
            return abort(403)

    url_prefix = '/admin'

    template_functions = {
        'pagetypes': 'pagetypes'
    }

    urls = {
        '/': 'index',
        '/draft/activate/<int:page_id>': 'draft_activate',
        '/draft/deactivate/<int:page_id>': 'draft_deactivate'
    }

    def index(self):
        return redirect(url_for('PagesCMSController.index'))

    def pagetypes(self):
        return SiteTree.pagetypes()

    @staticmethod
    def draft_activate(page_id=None):
        session["draft"] = True
        if page_id:
            page = db.session.query(SiteTree).get(page_id)
            if page:
                redirect_url = page.get_url()
                return redirect(redirect_url)
        return redirect("/")

    @staticmethod
    def draft_deactivate(page_id=None):
        session["draft"] = False
        if page_id:
            page = db.session.query(SiteTree.LiveType).get(page_id)
            if page:
                redirect_url = page.get_url()
                return redirect(redirect_url)
        return redirect("/")

class PagesCMSController(CMSController):
    url_prefix = CMSController.url_prefix + '/pages'

    urls = {
        '/tree': 'sitetree',
        '/tree/sort': 'sitetree_sort',
        '/': 'index',
        '/<int:page_id>/edit': 'edit_page',
        '/add/<page_type>': 'add_page'
    }

    allowed_actions = [
        'add_page', 'edit_page', 'sitetree_sort'
    ]

    def index(self):
        return render_template("page/index.html")

    def sitetree(self):
        s = SiteTree.get_sitetree()
        print(s)
        resp = make_response(json.dumps(s), 200)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def sitetree_sort(self):
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


    def edit_page(self, page_id):
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
                               page_form=page_form,
                               cms_title=page.name)

    def add_page(self, page_type):
        import silverflask.models.models as models

        _class = getattr(models, page_type)
        page = _class()
        page.name = "New Page"

        parent_id = request.args.get('parent', None)
        if parent_id:
            page.parent_id = int(parent_id)

        page_form = page.get_cms_form()
        page_form = page_form()
        page_form.process(request.form, obj=page)

        if page_form.validate_on_submit():
            page_form.populate_obj(page)
            db.session.add(page)
            db.session.commit()
            return redirect(url_for(".edit_page", page_id=page.id))

        return render_template("page/edit.html",
                               page_form=page_form)


class DataObjectCMSController(CMSController):
    url_prefix = CMSController.url_prefix + '/data_object'
    urls = {
        '/add/<cls>': 'add',
        '/edit/<cls>/<int:id_>': 'edit',
    }
    allowed_actions = ['add', 'edit']


    def add(self, cls):
        import silverflask.models.models as models

        _class = getattr(models, cls)
        do = _class()

        relation_id = request.args.get('relation_id', None)
        if relation_id:
            do.page_id = int(relation_id)

        form = do.get_cms_form()
        form = form()
        form.process(request.form, obj=do)

        if form.validate_on_submit():
            form.populate_obj(do)
            db.session.add(do)
            db.session.commit()
            # return redirect(url_for(".edit", page_id=do.id))

        return render_template("page/edit.html",
                               page_form=form)

    def edit(self, cls, id_):
        import silverflask.models.models as models

        _class = getattr(models, cls)
        do = _class.query.get_or_404(id_)

        form = do.get_cms_form()
        form = form()
        form.process(request.form, obj=do)

        if form.validate_on_submit():
            form.populate_obj(do)
            db.session.add(do)
            db.session.commit()
            # return redirect(url_for(".edit", page_id=do.id))

        return render_template("page/edit.html",
                               page_form=form)

from silverflask.models.FileObject import create_file
from silverflask.models import FileObject
from silverflask.fields import GridField
from flask import jsonify
from flask_wtf import Form


class FilesCMSController(CMSController):
    url_prefix = CMSController.url_prefix + '/files'
    urls = {
        '/': 'index',
        '/upload': 'upload',
        '/file/<int:file_id>/delete': 'delete_file'
    }

    allowed_actions = [
        'upload'
    ]

    def index(self):
        class AssetsForm(Form):
            gridfield = GridField(
                buttons=[],
                display_cols=["id", "name"],
                query=FileObject.query,
                controlled_class=FileObject
            )

        form = AssetsForm()
        return render_template("assetmanager.html", form=form)


    def upload(self):
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

    def delete_file(self, file_id):
        fo = FileObject.query.get(file_id)
        fo.delete_file_and_self()

