from pltypeerror import plTypeError
from pltypes.checkabletype import CheckableType


class NoType(CheckableType):
    """
    Always fails a type check for any type.
    """
    def check(self, obj, var_name):
        raise plTypeError(var_name, type(obj).__name__, str(self), obj)
