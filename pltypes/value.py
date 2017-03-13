import copy


def value(clazz):
    """
    Provide standard methods for a class that holds
    member variables and has value semantics.
    """
    ret = copy.deepcopy(clazz)
    ret.__repr__ = lambda self: "%s()" % clazz.__name__
    ret.__str__ = lambda self: repr(self)
    return ret
