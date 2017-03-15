from type_check import type_check
from pltypes.peekable import Peekable
from pstring import pString


def lex_string(chars):
    type_check(Peekable(), chars, "chars")
    first = next(chars)
    if first != '"':
        return None
    try:
        ret = ""
        while chars.peek() != '"':
            ret += next(chars)
        next(chars)
    except StopIteration:
        pass
    return pString(value=ret)
