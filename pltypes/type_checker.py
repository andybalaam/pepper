from pltypeerror import plTypeError


import copy


def _check(self, obj, var_name):
    assert type(var_name) == str
    if not self.matches(obj):
        raise plTypeError(var_name, type(obj).__name__, str(self), obj)


def type_checker(clazz):
    """
    Given a class with a matches() method, make
    it be a Checkable by providing a check()
    method that calls matches() to decide
    whether the type matches.
    """
    assert type(clazz) == type
    ret = copy.deepcopy(clazz)
    ret.check = _check
    return ret
