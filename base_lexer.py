import itertools
import re

from pclosebracket import pCloseBracket
from popenbracket import pOpenBracket
from psymbol import pSymbol
from ptoken import pToken
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from type_check import type_check


def lex_punctuation(chars):
    ch = next(chars)
    type_check(Iterable(plChar()).item_type, ch, "chars")
    if ch == "(":
        return pOpenBracket(), ""
    elif ch == ")":
        return pCloseBracket(), ""
    else:
        return None, ch


symbol_char_re_ = re.compile("[a-zA-Z0-9_]")


def lex_symbol(chars):
    ret = ""
    backtrackchars = ""
    for ch in chars:
        type_check(Iterable(plChar()).item_type, ch, "chars")
        if symbol_char_re_.match(ch):
            ret += ch
        else:
            backtrackchars = ch
            return pSymbol(ret), backtrackchars
    if len(ret) > 0:
        return pSymbol(ret), ""
    else:
        raise StopIteration()


def lex(chars):
    type_check(Iterable(plChar()), chars, "chars")

    backtrackchars = ""
    it = iter(chars)
    while True:
        for fn in [lex_punctuation, lex_symbol]:
            tok, backtrackchars = fn(itertools.chain(backtrackchars, it))
            if tok is not None:
                assert isinstance(tok, pToken)
                yield tok
                break
