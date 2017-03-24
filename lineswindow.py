from type_check import type_check
from pltypes.iterable import Iterable
from pltypes.plchar import plChar


class LinesWindow:
    r"""
    Allows iterating through an iterable of characters
    and provides the previous N and next N lines when asked.

    >>> from itertools import islice
    >>> it = LinesWindow("ab\nc\ne\ng\nij\nkl\nmn\nop\nqr\nst\n", "it")
    >>> list(islice(it, 12))
    ['a', 'b', '\n', 'c', '\n', 'e', '\n', 'g', '\n', 'i', 'j', '\n']
    >>> next(it)
    'k'
    >>> it.before()
    'c\ne\ng\nij\nk'
    >>> it.after()
    'l\nmn\nop\nqr\n'
    >>> it = LinesWindow("a\nd\n", "it")
    >>> next(it); next(it); next(it); next(it)
    'a'
    '\n'
    'd'
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
        self._before = []
        self._current = ""

    def __iter__(self):
        return self

    def __next__(self):
        ret = next(self.chars)
        type_check(Iterable(plChar()).item_type, ret, self.var_name)
        self._current += ret
        if ret == "\n":
            self._before.append(self._current)
            self._before = self._before[-4:]
            self._current = ""
        return ret

    def before(self):
        return "".join(self._before) + self._current

    def after(self):
        ret = ""
        lines = 0
        for ch in self.chars:
            ret += ch
            if ch == "\n":
                lines += 1
                if lines > 3:
                    break
        return ret
