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

    def __getitem__(self, item):
        i = self.find_by_name(item)
        if not i:
            raise(IndexError("No item named %s" % item))
        return i

    def __delitem__(self, item):
        def delete_unbound_child(tab):
            for c in tab.unbound_children:
                if c.kwargs["name"] == item:
                    tab.unbound_children.remove(c)
                    return True
            for t in tab.tabs:
                return delete_unbound_child(t)

        ret_val = delete_unbound_child(self.root)

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

    def find_by_name(self, name, tab=None, unbound=False):
        if not tab:
            tab = self.root
        print(tab, tab.tabs)
        for c in tab.children:
            print(c.name, name)
            if c.name == name:
                return c
        for t in tab.tabs:
            elem = self.find_by_name(name, t)
            if elem:
                return elem
        return None

    def add_to_tab(self, tabname, field, before=None):
        fieldname = field.kwargs["name"]
        try:
            del self[fieldname]
        except IndexError:
            pass

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
        return returnlist

    def __iter__(self):
        yield self.items()

class OrderedForm(Form):
    """
    An extension to the generic WTForm that can keep track of sorting in a manner different from the general
    usage pattern of WTForms.

    This class is useful for usage inside the CMS where its nice to not having to repeat all form code everytime.
    It is a "forms-just-work approach".

    The form is split into tabs. There is always a ``Root`` tab where all form elements and tabnodes are attached to.
    E.g. ::

        form = type(PageOrderedForm, (OrderedForm, ), {})
        form.add_to_tab("Root.Main", new StringField("abc", name="abc"))
        form.add_to_tab("Root.Main", new StringField("def", name="def"), "abc")
        form.add_to_tab("Root.Settings", new BooleanField("booleansetting", name="booleansetting"))
        return form

    """
    _fields = OrderedFieldList()
    tabbed_form = True

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
                c = bind_fields(t)
                if c == 0:
                    print(t)
                    print(t.name)
                    del t
                    print(tab.children)
            return len(tab.children)


        bind_fields(self._fields.root)
        self.process(formdata, obj, data)

    @classmethod
    def add_to_tab(cls, tabname, field, before=None):
        """
        Adds a form field to a tab.
        :param tabname: The tabname is a dot-delimited tab location. The tab name should be a camel cased name. ``Root``
                        is always existing and always the root tab.
                        Examples: ``Root.Main``, ``Root.PageContent``, ``Root.Main.ImageGallery``
        :param field:   An instantiated WTForm field. Note that field names have to be unique to the form
        :param before:  Optional: sort the field before another field if it exists in a specific tab.
        :return:        None
        """
        return cls._fields.add_to_tab(tabname, field, before)

    def get_tab(self, location):
        """
        Get a specific tab by name indicator
        :param location: e.g. ``Root.Main``
        :return:
        """
        return self._fields.get_tab(location)

    def get_root(self):
        """
        Get root tab
        :return: root tab
        """
        return self._fields.root

    def get_field(self, field_name):
        """
        Find a specific field by name in all tabs
        :param field_name: name of the field
        :return:
        """
        all_fields = self._fields.items(self._fields.root)
        print("all_fields", all_fields)
        for name, field in all_fields:
            print(name, field_name)
            if name == field_name:
                return field


class OrderedFormFactory:
    def __init__(self):
        self.fields = OrderedFieldList()
    def __call__(self, *args, **kwargs):
        return self.create()(*args, **kwargs)

    def create(self):
        return type('OrderedFactoryForm', (OrderedForm, ), {
            "_fields": self.fields
        })

    def add_to_tab(self, tabname, field, before=None):
        """
        Adds a form field to a tab.
        :param tabname: The tabname is a dot-delimited tab location. The tab name should be a camel cased name. ``Root``
                        is always existing and always the root tab.
                        Examples: ``Root.Main``, ``Root.PageContent``, ``Root.Main.ImageGallery``
        :param field:   An instantiated WTForm field. Note that field names have to be unique to the form
        :param before:  Optional: sort the field before another field if it exists in a specific tab.
        :return:        None
        """
        return self.fields.add_to_tab(tabname, field, before)
