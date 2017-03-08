import itertools
import re

from lexfailure import LexFailure
from pclosebracket import pCloseBracket
from popenbracket import pOpenBracket
from psymbol import pSymbol
from ptoken import pToken
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from type_check import type_check
from windowediterator import WindowedIterator


def lex_punctuation(chars):
    ch = next(chars)
    if ch == "(":
        return pOpenBracket()
    elif ch == ")":
        return pCloseBracket()
    else:
        return None


begin_symbol_char_re_ = re.compile("[a-zA-Z_]")
symbol_char_re_ = re.compile("[a-zA-Z0-9_]")


def lex_symbol(chars):
    ch = chars.peek()
    if not begin_symbol_char_re_.match(ch):
        return None

    ret = ""
    while True:
        try:
            ch = chars.peek()
        except StopIteration as e:
            if len(ret) > 0:
                return pSymbol(ret)
            else:
                raise e

        if symbol_char_re_.match(ch):
            ret += next(chars)
        else:
            return pSymbol(ret)


def _next_token(it):
    for fn in [lex_punctuation, lex_symbol]:
        tok = fn(it)
        if tok is None:
            it.back()   # This lexer failed - backtrack
        else:
            assert isinstance(tok, pToken)
            it.mark()   # This lexer found a token
            return tok
    return None


def lex(chars):
    type_check(Iterable(plChar()), chars, "chars")
    it = WindowedIterator(chars, Iterable(plChar()).item_type, "chars")
    try:
        while True:
            tok = _next_token(it)
            if tok is not None:
                yield tok
            else:
                raise LexFailure()
    except StopIteration:
        pass  # Finished iterating, exit normally
