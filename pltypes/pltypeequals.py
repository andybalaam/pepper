from pltypeerror import plTypeError
from pltypes.checkabletype import CheckableType


class plTypeEquals(CheckableType):
    def __init__(self, type_):
        assert type(type_) == type
        self.type_ = type_

    def check(self, obj, var_name):
        assert isinstance(var_name, str)
        if type(obj) != self.type_:
            raise plTypeError(
                var_name,
                str(type(obj)),
                str(self),
                obj
            )

    def name(self):
        return self.type_.__name__
