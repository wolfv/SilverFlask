from .cms import bp
from flask import abort, request, jsonify, render_template
from silverflask import db

def get_gridfield_context(cls, record_id, formname, fieldname, id=None):
    pass

def gridfield_get_return_dict(query, cls, record_id, formname, fieldname):
    data = [r.as_dict() for r in query()]
    print(data)
    for d in data:
        d["edit_url"] = "/admin/gridfield/{0}/{1}/{2}/{3}/edit/{4}".format(cls, record_id, formname, fieldname, d["id"])
        d["DT_RowId"] = str(d["id"])
    return data

@bp.route("/gridfield/<cls>/<int:record_id>/<formname>/<fieldname>", methods=["GET", "POST"])
def gridfield_response(cls, record_id, formname, fieldname):
    from silverflask import models
    _class = getattr(models, cls)
    inst = _class.query.get(record_id)
    # if not inst:
    #     abort("Not Found", 404query=db.session.query(FileObject).all)
    form = getattr(inst, formname)()
    field = getattr(form, fieldname)
    query = field.kwargs["query"]
    data = gridfield_get_return_dict(query, cls, record_id, formname, fieldname)
    return jsonify(data=data)


@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/add", methods=["GET", "POST"])
def gridfield_add_record(cls, record_id, form, fieldname):
    from silverflask import models
    _class = getattr(models, cls)
    inst = _class.query.get(record_id)
    # if not inst:
    # abort("Not Found", 404)
    form = getattr(inst, form)()
    field = getattr(form, fieldname)
    query = field.kwargs["query"]()
    elem = query.column_descriptions[0]["type"]()
    print(elem)
    elem.page_id = record_id
    element_form = elem.get_cms_form()
    element_form_instance = element_form(request.form, obj=elem)
    if element_form_instance.validate_on_submit():
        element_form_instance.populate_obj(elem)
        db.session.add(elem)
        print(elem.__dict__)
        db.session.commit()
        return "elem " + str(elem.__dict__)
    element_form.page_id.kwargs["default"] = record_id

    return render_template("add_page.html",
                           page_form=element_form_instance)


@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/edit/<int:id>", methods=["GET", "POST"])
def gridfield_edit_record(cls, record_id, form, fieldname, id):
    from silverflask import models
    _class = getattr(models, cls)
    inst = _class.query.get(record_id)
    # if not inst:
    # abort("Not Found", 404)
    form = getattr(inst, form)()
    field = getattr(form, fieldname)
    query = field.kwargs["query"]()
    elem = query.column_descriptions[0]["type"]
    elem = db.session.query(elem).get(id)
    element_form = elem.get_cms_form()
    element_form_instance = element_form(request.form, obj=elem)
    if element_form_instance.validate_on_submit():
        element_form_instance.populate_obj(elem)
        db.session.commit()

    return render_template("add_page.html",
                           page_form=element_form_instance)

@bp.route("/gridfield/<cls>/<int:record_id>/<form>/<fieldname>/sort", methods=["POST"])
def gridfield_sort_record(cls, record_id, form, fieldname):
    from silverflask import models
    to = int(request.form["toPosition"])
    _id = int(request.form["id"])
    _class = getattr(models, cls)
    inst = _class.query.get(record_id)

    # if not inst:
    # abort("Not Found", 404)
    form = getattr(inst, form)()
    field = getattr(form, fieldname)
    query = field.kwargs["query"]()
    elem = query.column_descriptions[0]["type"]
    print(elem.default_order)
    prev_elem = query.offset(to - 1).first()
    print("\n\n %i \n\n" % prev_elem.sort_order)
    curr_elem = db.session.query(elem).get(_id)
    curr_elem.move_after(to)
    db.session.commit()
    data = gridfield_get_return_dict(lambda: query, cls, record_id, form, fieldname)
    return jsonify(data=data)
    # element_form = elem.get_cms_form()
    return "OK"

    # element_form_instance = element_form(request.form, obj=elem)
    # if element_form_instance.validate_on_submit():
    #     element_form_instance.populate_obj(elem)
    #     db.session.commit()
