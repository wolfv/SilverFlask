from flask import render_template as flask_render_template
from flask import request, abort

from flask_wtf import Form

def render_template(template, *args, **kwargs):
    if request.method == 'GET' and request.args.get('form') and request.args.get('field'):
        form = kwargs.get(request.args['form'])
        field = form[request.args.get('field')]
        action = request.args.get('action')
        if not form or not field or not action:
            abort(404)
        print("There was a method on a form requested here!")
        return getattr(field.controller_class(field, form), action)()
    for key, item in kwargs.items():
        print(type(item))
        if issubclass(item.__class__, (Form, )):
            print("We have a form!")
            for field_item in item._fields.items():
                print(field_item)

                if hasattr(field_item[1], 'controller_class'):
                    print("WE HAVE A CONTROLLER >>> >> >>> >>")
                    field_item[1].widget.generate_urls(form_name=key, field_name=field_item[0])
    return flask_render_template(template, *args, **kwargs)