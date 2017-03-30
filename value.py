import copy


from type_check import type_check


def init_(self, arg_types, **kwargs):
    for name in arg_types.keys():
        v = kwargs[name]
        type_check(arg_types[name], v, name)
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


def value(**kwargs):
    """
    Provide standard methods for a class that holds
    member variables and has value semantics.
    """
    return ValueModifier(kwargs)
