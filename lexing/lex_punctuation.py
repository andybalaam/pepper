from charsiterable import CharsIterable
from pltypes.peekable import Peekable
from pltypes.plchar import plChar
from tokens.pclosebracket import pCloseBracket
from tokens.pequalssign import pEqualsSign
from tokens.popenbracket import pOpenBracket
from tokens.psemicolon import pSemicolon
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
    elif ch == "=":
        return pEqualsSign()
    else:
        return None
