from pltypes.checkabletype import CheckableType
from pltypes.pltypeequals import plTypeEquals
from pltypeerror import plTypeError


class Iterable(CheckableType):
    class ItemType(CheckableType):
        def __init__(self, parent, type_):
            assert isinstance(parent, Iterable)
            # type_ is not always CheckableType, when we are
            #       building error messages
            self.parent = parent
            self.type_ = type_

        def check(self, obj, var_name):
            assert isinstance(var_name, str)
            try:
                self.type_.check(obj, var_name)
            except plTypeError:
                raise plTypeError(
                    var_name,
                    str(Iterable(plTypeEquals(type(obj)))),
                    str(self.parent),
                    obj
                )

        def name(self):
            return type(self).__name__

    def __init__(self, type_):
        self.type_ = type_
        self.item_type = Iterable.ItemType(self, type_)

    def check(self, obj, var_name):
        try:
            iter(obj)
        except:
            raise plTypeError(var_name, type(obj).__name__, str(self), obj)

    def name(self):
        return type(self).__name__

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s(%s)" % (self.name(), self.type_.name())
