import re
from pltypes.iterable import Iterable
from pltypes.peekable import Peekable
from pltypes.plchar import plChar
from psymbol import pSymbol
from type_check import type_check

begin_symbol_char_re_ = re.compile("[a-zA-Z_]")
symbol_char_re_ = re.compile("[a-zA-Z0-9_]")


def lex_symbol(chars):
    type_check(Iterable(plChar()), chars, "chars")
    type_check(Peekable(), chars, "chars")
    ch = chars.peek()
    type_check(Iterable(plChar()).item_type, ch, "chars")
    if not begin_symbol_char_re_.match(ch):
        return None

    ret = ""
    while True:
        try:
            ch = chars.peek()
            type_check(Iterable(plChar()).item_type, ch, "chars")
        except StopIteration as e:
            if len(ret) > 0:
                return pSymbol(ret)
            else:
                raise e

        if symbol_char_re_.match(ch):
            ret += next(chars)
        else:
            return pSymbol(ret)
