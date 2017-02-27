from psymbol import pSymbol
from pltypeerror import plTypeError


class plChar:
    pass


def iterable(type_):
    pass


def lex(chars):
    if chars.__class__ != str:
        raise plTypeError("chars", chars, iterable(plChar))
    yield pSymbol(chars)
