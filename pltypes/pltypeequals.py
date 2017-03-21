from pltypes.type_checker import type_checker


@type_checker
class plTypeEquals:
    def __init__(self, type_):
        assert type(type_) == type
        self.type_ = type_

    def matches(self, obj):
        return type(obj) == self.type_

    def __str__(self):
        return str(self.type_)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, repr(self.type_))


# Can't use type_check because of circular dependencies
assert hasattr(plTypeEquals(int), "check")
