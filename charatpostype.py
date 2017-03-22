from pltypes.type_checker import type_checker


@type_checker
class CharAtPosType:
    def matches(self, other):
        return (
            hasattr(other, "char") and
            hasattr(other, "pos") and
            type(other.pos) == tuple and
            len(other.pos) == 2
        )
