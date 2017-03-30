from pltypes.checkable import Checkable
from type_check import type_check
from value import value


@value()
class AnyType:
    """
    Always passes any type check.
    """
    def check(self, obj, var_name):
        pass


type_check(Checkable(), AnyType(), "AnyType")
