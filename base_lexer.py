from psymbol import pSymbol
from pltypeerror import plTypeError


class plChar:
    pass


class Iterable:
    def __init__(self, type_):
        self.type_ = type_

    def __str__(self):
        return "Iterable(%s)" % self.type_.__name__


def lex(chars):
    if chars.__class__ != str:
        raise plTypeError("chars", chars, Iterable(plChar))
    yield pSymbol(chars)
