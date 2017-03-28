from pltypes.checkable import Checkable
from pltypes.type_checker import type_checker
from pltypes.value import value
from pltypeerror import plTypeError
from type_check import type_check


@type_checker
@value(size=int, type_=type)
class plTuple:
    def matches(self, obj):
        return (
            isinstance(obj, tuple) and
            len(obj) == self.size and
            isinstance(obj[0], self.type_)
        )


type_check(Checkable(), plTuple(size=3, type_=int), "plTuple")
