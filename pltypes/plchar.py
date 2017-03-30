from pltypes.checkable import Checkable
from pltypes.type_checker import type_checker
from pltypeerror import plTypeError
from type_check import type_check
from value import value


@type_checker
@value()
class plChar:
    def matches(self, obj):
        return (
            isinstance(obj, str) and
            len(obj) == 1
        )


type_check(Checkable(), plChar, "plChar")
