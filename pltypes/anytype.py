from pltypes.checkable import Checkable
from pltypes.value import value
from type_check import type_check


@value
class AnyType:
    """
    Always passes any type check.
    """
    def check(self, obj, var_name):
        pass


type_check(Checkable(), AnyType(), "AnyType")
