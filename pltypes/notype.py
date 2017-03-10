from pltypes.checkable import Checkable
from pltypes.type_checker import type_checker
from pltypes.value import value
from pltypeerror import plTypeError
from type_check import type_check


@type_checker
@value
class NoType:
    """
    Always fails a type check for any type.
    """
    def matches(self, obj):
        return False


type_check(Checkable(), NoType(), "NoType")
