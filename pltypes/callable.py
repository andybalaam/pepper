from pltypes.checkable import Checkable
from pltypeerror import plTypeError
from type_check import type_check
from value import value


@value
class Callable:
    def check(self, obj, var_name):
        if not callable(obj):
            raise plTypeError(var_name, type(obj).__name__, str(self), obj)


type_check(Checkable(), Callable(), "Callable")
