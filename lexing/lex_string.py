from charsiterable import CharsIterable
from type_check import type_check
from pltypes.peekable import Peekable
from tokens.pstring import pString


def lex_string(chars):
    type_check(CharsIterable(), chars, "chars")
    type_check(Peekable(), chars, "chars")
    first = next(chars).char
    if first != '"':
        return None
    try:
        ret = ""
        while chars.peek().char != '"':
            ret += next(chars).char
        next(chars)
    except StopIteration:
        pass
    return pString(value=ret)
