from charatpostype import CharAtPosType
from pltypes.checkable import Checkable
from pltypes.iterable import Iterable
from type_check import type_check


def CharsIterable():
    return Iterable(CharAtPosType())


type_check(Checkable(), CharsIterable(), "CharsIterable")
