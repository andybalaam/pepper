from pltypes.hasmethod import hasmethod
from pltypes.type_checker import type_checker
from type_check import type_check
from value import value


@type_checker
@value()
class Checkable:
    """
    A type checker that checks that the supplied object
    is itself a type checker!
    """

    def matches(self, obj):
        return hasmethod(obj, "check")


# Ironically, check that we ourselves are a type checker
type_check(Checkable(), Checkable(), "Checkable")
