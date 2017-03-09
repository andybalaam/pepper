from lexing.lexfailure import LexFailure
from ptoken import pToken
from pltypes.backable import Backable
from pltypes.callable import Callable
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from type_check import type_check
from windowediterator import WindowedIterator


def _next_token(chars, lex_fns):
    type_check(Backable(), chars, "chars")
    for fn in lex_fns:
        type_check(Iterable(Callable()).item_type, fn, "lex_fns")
        tok = fn(chars)
        if tok is None:
            chars.back()   # This lexer failed - backtrack
        else:
            assert isinstance(tok, pToken)
            chars.mark()   # This lexer found a token
            return tok
    return None


def base_lex(chars, lex_fns):
    type_check(Iterable(plChar()), chars, "chars")
    type_check(Iterable(Callable()), lex_fns, "lex_fns")
    it = WindowedIterator(chars, Iterable(plChar()).item_type, "chars")
    try:
        while True:
            tok = _next_token(it, lex_fns)
            if tok is not None:
                yield tok
            else:
                raise LexFailure()
    except StopIteration:
        pass  # Finished iterating, exit normally
