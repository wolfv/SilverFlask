from .cms import bp
from flask import abort, request, jsonify, render_template
from silverflask import db
from silverflask.models.OrderedForm import OrderedFormFactory

def get_gridfield_context(cls, record_id, formname, fieldname, id=None):
    from silverflask import models
    _class = getattr(models, cls)
    inst = db.session.query(_class).get(record_id)
    form = getattr(inst, formname)()
    if type(form) == OrderedFormFactory:
        form = form.create()
    forminstance = form()
    field, query = None, None
    if form.tabbed_form:
        field = forminstance.get_field(fieldname)
        query = field.query()
    else:
        field = getattr(forminstance, fieldname)
        query = field.kwargs["query"]()

    elem = query.column_descriptions[0]["type"]()
    return elem, forminstance, field, query

def gridfield_get_return_dict(query, cls, record_id, formname, fieldname):
    data = [r.as_dict() for r in query]
    print(data)
    for d in data:
        d["edit_url"] = "/admin/gridfield/{0}/{1}/{2}/{3}/edit/{4}".format(cls, record_id, formname, fieldname, d["id"])
        d["DT_RowId"] = str(d["id"])
    return data

@bp.route("/gridfield/<cls>/<int:record_id>/<formname>/<fieldname>", methods=["GET", "POST"])
def gridfield_response(cls, record_id, formname, fieldname):
    elem, forminstance, field, query = get_gridfield_context(cls, record_id, formname, fieldname)
    data = gridfield_get_return_dict(query, cls, record_id, formname, fieldname)
    return jsonify(data=data)


@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/add", methods=["GET", "POST"])
def gridfield_add_record(cls, record_id, form, fieldname):
    elem, forminstance, field, query = get_gridfield_context(cls, record_id, form, fieldname)
    print(elem)
    elem.page_id = record_id
    element_form = elem.get_cms_form()
    element_form_instance = element_form(request.form, obj=elem)
    if element_form_instance.validate_on_submit():
        element_form_instance.populate_obj(elem)
        db.session.add(elem)
        db.session.commit()
        return "elem " + str(elem.__dict__)
    element_form.page_id.kwargs["default"] = record_id

    return render_template("page/add.html",
                           page_form=element_form_instance)


@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/edit/<int:id>", methods=["GET", "POST"])
def gridfield_edit_record(cls, record_id, form, fieldname, id):
    elem, forminstance, field, query = get_gridfield_context(cls, record_id, form, fieldname)
    elem = query.column_descriptions[0]["type"]
    elem = db.session.query(elem).get(id)
    element_form = elem.get_cms_form()
    element_form_instance = element_form(request.form, obj=elem)
    if element_form_instance.validate_on_submit():
        element_form_instance.populate_obj(elem)
        db.session.commit()

    return render_template("page/add.html",
                           page_form=element_form_instance)


@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/sort", methods=["POST"])
def gridfield_sort_record(cls, record_id, form, fieldname):
    elem, forminstance, field, query = get_gridfield_context(cls, record_id, form, fieldname)

    to = int(request.form["toPosition"])
    _id = int(request.form["id"])

    elem_type = query.column_descriptions[0]["type"]
    prev_elem = query.offset(to - 1).first()

    curr_elem = db.session.query(elem_type).get(_id)
    curr_elem.move_after(to)

    db.session.commit()
    data = gridfield_get_return_dict(query, cls, record_id, form, fieldname)
    return jsonify(data=data)
    # element_form = elem.get_cms_form()
    return "OK"

    # element_form_instance = element_form(request.form, obj=elem)
    # if element_form_instance.validate_on_submit():
    #     element_form_instance.populate_obj(elem)
    #     db.session.commit()
