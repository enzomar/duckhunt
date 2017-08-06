from functools import wraps
import jsonpickle


def json_str(cls):
    c_str = jsonpickle.encode(cls, unpicklable=False)
    return c_str.replace('\"__', '\"')


def getter_setter_gen(name, type_):
    def getter(self):
        try:
            return getattr(self, "__" + name)
        except AttributeError:
            return None

    def setter(self, value):
        if not isinstance(value, type_):
            raise TypeError(
                "%s attribute must be set to an instance of %s" % (name, type_))
        setattr(self, "__" + name, value)
    return property(getter, setter)


def frozen_setattr(cls, key, value):
    try:
        cls.__frozen_attrs[key](cls, key, value)
    except KeyError:
        raise AttributeError("%s attribute has not been declared" % (key))


def duckhunt(cls):
    new_dct = dict()
    frozen_attrs = dict()
    for key, value in cls.__dict__.items():
        # print key, value
        if isinstance(value, type):
            # print '  ',value
            value = getter_setter_gen(key, value)
        new_dct[key] = value
        frozen_attrs[key] = object.__setattr__
        frozen_attrs['__' + key] = object.__setattr__

    # remove __dict__ key 0> fix pickle issue
    del new_dct['__dict__']

    # Creates a new class, using the modified dictionary as the class dict:
    n = type(cls.__name__, cls.__bases__, new_dct)
    n.__setattr__ = frozen_setattr
    n.__str__ = json_str
    n.__frozen_attrs = frozen_attrs
    return n
