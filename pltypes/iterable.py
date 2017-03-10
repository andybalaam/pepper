from pltypes.checkable import Checkable
from pltypes.pltypeequals import plTypeEquals
from pltypeerror import plTypeError
from type_check import type_check


class Iterable:
    class ItemType:
        def __init__(self, parent, type_):
            assert isinstance(parent, Iterable)
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


type_check(Checkable(), Iterable(int), "Iterable")
type_check(Checkable(), Iterable(int).item_type, "Iterable.item_type")
