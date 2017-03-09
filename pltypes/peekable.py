from pltypes.checkabletype import CheckableType


class Peekable(CheckableType):
    def check(self, obj, var_name):
        if not hasattr(obj, "peek"):
            raise plTypeError(var_name, type(obj).__name__, str(self), obj)

    def name(self):
        return type(self).__name__

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s()" % self.name()
