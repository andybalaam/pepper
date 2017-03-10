from pltypes.checkable import Checkable
from pltypes.value import value
from pltypeerror import plTypeError
from type_check import type_check


@value
class Callable:
    def check(self, obj, var_name):
        if not callable(obj):
            raise plTypeError(var_name, type(obj).__name__, str(self), obj)


type_check(Checkable(), Callable(), "Callable")
