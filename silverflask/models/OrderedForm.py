from flask_wtf import Form
from wtforms.meta import DefaultMeta
from flask import current_app

class TabNode():

    def __init__(self, name):
        self.name = name
        self.unbound_children = []
        self.tabs = []
        self.children = []

    def get_tab(self, tabname):
        for c in self.tabs:
            if c.name == tabname:
                return c
        return None

    def find(self, name):
        idx = 0
        for idx, child in enumerate(self.unbound_children):
            if child.kwargs.get("name") == name:
                return idx
        return len(self.unbound_children)

class OrderedFieldList():
    def __init__(self):
        self.root = TabNode("Root")

    def get_tab(self, location, create_tabs=False):
        location = location.split('.')
        print(location)
        node = prev_node = self.root

        if location[0] == "Root":
            del location[0]
        else:
            raise UserWarning("Error: Root must be in location")

        for l in location:
            node = prev_node.get_tab(l)
            if not node and not create_tabs:
                raise(IndexError("Tab %r not found!" % location))
                return None
            elif not node and create_tabs:
                node = TabNode(l)
                prev_node.tabs.append(node)
            prev_node = node

        return node


    def add_to_tab(self, tabname, field, before=None):

        def find_by_name(name, tab):
            for c in tab.children:
                if c.name == name:
                    return c
            for t in tab.tabs:
                return find_by_name(name, t)
            return None

        existing_child = find_by_name(field.kwargs["name"], self.root)
        if existing_child:
            del existing_child

        node = self.get_tab(tabname, True)
        index = node.find(before)
        node.unbound_children.insert(index, field)

    def items(self, tab=None):
        returnlist = []
        def append_items(tab):
            for c in tab.children:
                returnlist.append((c.name, c))
            for t in tab.tabs:
                append_items(t)

        append_items(tab if tab else self.root)
        print(returnlist)
        return returnlist

    def __iter__(self):
        yield self.items()

class OrderedForm(Form):
    _fields = OrderedFieldList()

    def __init__(self, formdata=None, obj=None, data=None, csrf_enabled=None, prefix='', meta=DefaultMeta()):

        if csrf_enabled is None:
            csrf_enabled = current_app.config.get('WTF_CSRF_ENABLED', True)

        self.csrf_enabled = csrf_enabled

        if self.csrf_enabled:
            if csrf_context is None:
                csrf_context = session
            if secret_key is None:
                # It wasn't passed in, check if the class has a SECRET_KEY
                secret_key = getattr(self, "SECRET_KEY", None)

            self.SECRET_KEY = secret_key
        else:
            csrf_context = {}
            self.SECRET_KEY = ''


        if prefix and prefix[-1] not in '-_;:/.':
            prefix += '-'

        self.meta = meta
        self._prefix = prefix
        self._errors = None

        translations = self._get_translations()
        extra_fields = []
        if meta.csrf:
            self._csrf = meta.build_csrf(self)
            extra_fields.extend(self._csrf.setup_form(self))

        def bind_fields(tab):
            tab.children = []
            for field in tab.unbound_children:
                name = field.kwargs["name"]
                del field.kwargs["name"]
                tab.children.append(field.bind(self, name))
            tab.unbound_children = []
            for t in tab.tabs:
                bind_fields(t)

        bind_fields(self._fields.root)
        self.process(formdata, obj, data)


    @classmethod
    def add_to_tab(cls, tabname, field, before=None):
        return cls._fields.add_to_tab(tabname, field, before)

    def get_tab(self, location):
        return self._fields.get_tab(location)

    def get_root(self):
        return self._fields.root