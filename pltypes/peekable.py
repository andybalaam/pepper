from pltypes.checkable import Checkable
from pltypes.type_checker import type_checker
from pltypes.value import value
from pltypeerror import plTypeError
from type_check import type_check


@type_checker
@value
class Peekable:
    def matches(self, obj):
        return hasattr(obj, "peek")


type_check(Checkable(), Peekable(), "Peekable")
