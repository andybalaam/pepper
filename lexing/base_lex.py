from charsiterable import CharsIterable
from lexing.lexfailure import LexFailure
from lineswindow import LinesWindow
from listing import listing
from pltypes.backable import Backable
from pltypes.callable import Callable
from pltypes.iterable import Iterable
from pltypes.plchar import plChar
from positionedcharacters import PositionedCharacters
from tokens.ptoken import pToken
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


def _num_newlines(s):
    return len(list(filter(lambda x: x == '\n', s)))


def base_lex(chars, lex_fns):
    type_check(CharsIterable(), chars, "chars")
    type_check(Iterable(Callable()), lex_fns, "lex_fns")
    lines_window = LinesWindow(chars, "chars")
    it = WindowedIterator(
        PositionedCharacters(lines_window, "lines_window"),
        CharsIterable().item_type,
        "it"
    )
    try:
        while True:
            tok = _next_token(it, lex_fns)
            if tok is not None:
                yield tok
            else:
                raise LexFailure(
                    it,
                    "I can't understand '%s'\n" +
                    "(it is not recognised by the lexer)."
                )
    except StopIteration:
        pass  # Finished iterating, exit normally
    except LexFailure as e:
        e.listing = listing(
            lines_window.before(), lines_window.after(), e.pos)
        e.file = "<stdin>"  # TODO
        raise e
