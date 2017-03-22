from charsiterable import CharsIterable
from pclosebracket import pCloseBracket
from pltypes.peekable import Peekable
from pltypes.plchar import plChar
from popenbracket import pOpenBracket
from psemicolon import pSemicolon
from type_check import type_check


def lex_punctuation(chars):
    type_check(CharsIterable(), chars, "chars")
    type_check(Peekable(), chars, "chars")
    char_at_pos = next(chars)
    type_check(CharsIterable().item_type, char_at_pos, "chars")
    ch = char_at_pos.char
    if ch == "(":
        return pOpenBracket()
    elif ch == ")":
        return pCloseBracket()
    elif ch == ";":
        return pSemicolon()
    else:
        return None
