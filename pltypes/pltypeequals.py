from pltypes.checkable import Checkable
from pltypes.type_checker import type_checker
from pltypeerror import plTypeError
from type_check import type_check


@type_checker
class plTypeEquals:
    def __init__(self, type_):
        assert type(type_) == type
        self.type_ = type_

    def check(self, obj, var_name):
        return type(obj) == self.type_

    def name(self):
        return self.type_.__name__

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, repr(self.type_))


type_check(Checkable(), plTypeEquals(int), "plTypeEquals")
