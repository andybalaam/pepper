from pltypes.checkable import Checkable
from pltypes.hasmethod import hasmethod
from pltypes.type_checker import type_checker
from pltypeerror import plTypeError
from type_check import type_check
from value import value


@type_checker
@value()
class Backable:
    def matches(self, obj):
        return (
            hasmethod(obj, "back") and
            hasmethod(obj, "mark")
        )


type_check(Checkable(), Backable(), "Backable")
