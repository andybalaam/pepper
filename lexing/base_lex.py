from lexing.lexfailure import LexFailure
from ptoken import pToken
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from type_check import type_check
from windowediterator import WindowedIterator


def _next_token(it, lex_fns):
    for fn in lex_fns:
        tok = fn(it)
        if tok is None:
            it.back()   # This lexer failed - backtrack
        else:
            assert isinstance(tok, pToken)
            it.mark()   # This lexer found a token
            return tok
    return None


def base_lex(chars, lex_fns):
    type_check(Iterable(plChar()), chars, "chars")
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
