
class classproperty(object):
    # adds @classproperty decorator
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
