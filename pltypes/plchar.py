from pltypeerror import plTypeError
from pltypes.checkabletype import CheckableType


class plChar(CheckableType):
    def check(self, obj, var_name):
        assert isinstance(var_name, str)
        if not isinstance(obj, str) or len(obj) != 1:
            raise plTypeError(
                var_name,
                str(type(obj)),
                str(self),
                obj
            )

    def name(self):
        return type(self).__name__
