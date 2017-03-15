from lexing.base_lex import base_lex
from lexing.lex_punctuation import lex_punctuation
from lexing.lex_string import lex_string
from lexing.lex_symbol import lex_symbol


lex_fns = [
    lex_punctuation,
    lex_symbol,
    lex_string,
]


def lex(chars):
    return base_lex(chars, lex_fns)
