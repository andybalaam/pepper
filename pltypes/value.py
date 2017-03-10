import copy


def value(clazz):
    """
    Provide standard methods for a class that holds
    member variables and has value semantics.
    """
    # ret = types.new_class(clazz.__name__, clazz.__bases__)
    ret = copy.deepcopy(clazz)
    ret.name = lambda self: type(self).__name__
    ret.__repr__ = lambda self: "%s()" % self.name()
    ret.__str__ = lambda self: repr(self)
    return ret
