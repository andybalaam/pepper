import itertools


class BacktrackingIterator:
    """
    Iterates through the supplied iterable, allowing you
    to backtrack.

    Call mark() to set a point to go back to (default
    is the start) and call back() to jump back to the
    last mark.

    >>> it = BacktrackingIterator("abc")
    >>> next(it)
    'a'
    >>> it.back()
    >>> next(it)
    'a'
    >>> next(it)
    'b'
    >>> it.mark()
    >>> next(it)
    'c'
    >>> it.back()
    >>> next(it)
    'c'
    >>> next(it)
    Traceback (most recent call last):
    StopIteration
    """

    def __init__(self, it):
        self.it = iter(it)
        self.backlog = []

    def __iter__(self):
        return self

    def __next__(self):
        ret = next(self.it)
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
