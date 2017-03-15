import copy


from pltypes.pltypeequals import plTypeEquals
from type_check import type_check


def mk_checkable(type_, name):
    if type(type_) == type:
        return plTypeEquals(type_)
    else:
        return type_


def init_(self, arg_types, **kwargs):
    for name in arg_types.keys():
        v = kwargs[name]
        type_check(mk_checkable(arg_types[name], name), v, name)
        self.__dict__[name] = v


def repr_(self, clazz):
    def impl(s):
        return "%s(%s)" % (
            clazz.__name__,
            ", ".join(
                "%s=%s" % (k, repr(s.__dict__[k])) for k in
                sorted(self.init_args.keys())
            )
        )
    return impl


def eq_(self):
    def impl(s, other):
        if type(s) != type(other):
            return False
        for arg_name in self.init_args:
            if s.__dict__[arg_name] != other.__dict__[arg_name]:
                return False
        return True
    return impl


class ValueModifier:
    def __init__(self, init_args):
        self.init_args = init_args

    def __call__(self, clazz):
        assert clazz is not None
        assert type(clazz) == type
        ret = copy.deepcopy(clazz)
        ret.__eq__ = eq_(self)
        ret.__repr__ = repr_(self, clazz)
        ret.__str__ = repr_(self, clazz)
        ret.__init__ = lambda s, **kwargs: init_(s, self.init_args, **kwargs)
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
