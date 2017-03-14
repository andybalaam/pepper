import copy


from pltypes.pltypeequals import plTypeEquals
from type_check import type_check


def mk_checkable(type_, name):
    if type(type_) == type:
        return plTypeEquals(type_)
    else:
        return type_


def init(self, arg_types, **kwargs):
    for name in arg_types.keys():
        v = kwargs[name]
        type_check(mk_checkable(arg_types[name], name), v, name)
        self.__dict__[name] = v


class ValueModifier:
    def __init__(self, init_args):
        self.init_args = init_args

    def __call__(self, clazz):
        assert clazz is not None
        assert type(clazz) == type
        ret = copy.deepcopy(clazz)
        ret.__repr__ = lambda s: "%s()" % clazz.__name__
        ret.__str__ = lambda s: repr(s)
        ret.__init__ = lambda s, **kwargs: init(s, self.init_args, **kwargs)
        return ret


def value(clazz=None, **kwargs):
    """
    Provide standard methods for a class that holds
    member variables and has value semantics.
    """
    if clazz is None:
        return ValueModifier(kwargs)
    else:
        return ValueModifier(kwargs)(clazz)
