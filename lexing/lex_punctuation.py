from pclosebracket import pCloseBracket
from pltypes.iterable import Iterable
from pltypes.peekable import Peekable
from pltypes.plchar import plChar
from popenbracket import pOpenBracket
from type_check import type_check


def lex_punctuation(chars):
    type_check(Iterable(plChar()), chars, "chars")
    type_check(Peekable(), chars, "chars")
    ch = next(chars)
    type_check(Iterable(plChar()).item_type, ch, "chars")
    if ch == "(":
        return pOpenBracket()
    elif ch == ")":
        return pCloseBracket()
    else:
        return None
