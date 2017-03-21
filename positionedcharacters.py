from type_check import type_check
from pltypes.iterable import Iterable
from pltypes.plchar import plChar


class CharAtPos:
    def __init__(self, char, column, line):
        type_check(plChar(), char, "char")
        type_check(int, column, "column")
        type_check(int, line, "line")

        self.char = char
        self.pos = (column, line)

    def __str__(self):
        return self.char


class PositionedCharacters:
    r"""
    Allows iterating through an iterable of characters
    and keeps track of what line and column you are at.

    >>> it = PositionedCharacters("abc\ndef\n", "it")
    >>> ch = next(it)
    >>> str(ch)
    'a'
    >>> ch.pos
    (1, 1)
    >>> ch = next(it)
    >>> str(ch)
    'b'
    >>> ch.pos
    (2, 1)
    >>> ch = next(it)
    >>> str(ch)
    'c'
    >>> ch = next(it)
    >>> str(ch)
    '\n'
    >>> ch.pos
    (4, 1)
    >>> ch = next(it)
    >>> str(ch), ch.pos
    ('d', (1, 2))
    >>> ch = next(it)
    >>> str(ch), ch.pos
    ('e', (2, 2))
    >>> str(next(it))
    'f'
    >>> str(next(it))
    '\n'
    >>> next(it)
    Traceback (most recent call last):
    StopIteration
    """

    def __init__(self, chars, var_name):
        type_check(Iterable(plChar), chars, "chars")
        type_check(str, var_name, "var_name")
        self.chars = iter(chars)
        self.var_name = var_name
        self.column = 1
        self.line = 1

    def __iter__(self):
        return self

    def __next__(self):
        ch = next(self.chars)
        type_check(Iterable(plChar()).item_type, ch, self.var_name)
        ret = CharAtPos(ch, self.column, self.line)
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ret
