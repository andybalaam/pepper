from type_check import type_check
import itertools


class WindowedIterator:
    """
    Iterates through the supplied iterable, allowing you
    to backtrack and peek.

    Call mark() to set a point to go back to (default
    is the start) and call back() to jump back to the
    last mark.

    Call it.peek() to see the item that will be returned
    by next(it).

    >>> from pltypes.anytype import AnyType
    >>> it = WindowedIterator("abc", AnyType(), "foo")
    >>> next(it)
    'a'
    >>> it.back()
    >>> next(it)
    'a'
    >>> it.peek()
    'b'
    >>> next(it)
    'b'
    >>> it.mark()
    >>> it.peek()
    'c'
    >>> next(it)
    'c'
    >>> it.back()
    >>> next(it)
    'c'
    >>> next(it)
    Traceback (most recent call last):
    StopIteration
    """

    def __init__(self, it, item_type, var_name):
        self.it = iter(it)
        self.item_type = item_type
        self.var_name = var_name
        self.backlog = []

    def __iter__(self):
        return self

    def __next__(self):
        ret = next(self.it)
        type_check(self.item_type, ret, self.var_name)
        self.backlog.append(ret)
        return ret

    def mark(self):
        """
        Mark a point to go back to next time we call back().
        Forgets the last point.
        """
        self.backlog = []

    def back(self):
        """
        Go back to the latest mark.
        """
        self.it = itertools.chain(self.backlog, self.it)
        self.backlog = []

    def peek(self):
        ret = next(self.it)
        type_check(self.item_type, ret, self.var_name)
        self.it = itertools.chain([ret], self.it)
        return ret
