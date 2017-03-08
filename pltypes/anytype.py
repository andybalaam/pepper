from pltypes.checkabletype import CheckableType


class AnyType(CheckableType):
    """
    Always passes any type check.
    """
    def check(self, obj, var_name):
        pass
