
class classproperty(object):
    # adds @classproperty decorator
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def uncamel(x):
    """
    from: http://stackoverflow.com/a/19940888, by TehTris
    """
    final = ''
    for item in x:
        if item.isupper():
            final += " " + item
        else:
            final += item
    if final[0] == "_":
        final = final[1:]
    return final
