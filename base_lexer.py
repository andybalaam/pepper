from psymbol import pSymbol
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from type_check import type_check


def lex(chars):
    chars_type = Iterable(plChar())
    type_check(chars_type, chars, "chars")
    for ch in chars:
        type_check(chars_type.item_type, ch, "chars")
    yield pSymbol(chars)
