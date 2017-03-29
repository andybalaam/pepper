from type_check import type_check
from windowediterator import WindowedIterator


class LexFailure(Exception):
    def __init__(self, chars, msg):
        type_check(WindowedIterator, chars, "chars")
        type_check(str, msg, "msg")

        self.tok = ""
        self.pos = None
        for ch in chars:
            if self.pos is None:
                self.pos = ch.pos
            if ch.char in " \n":
                break
            self.tok += ch.char

        self.msg = msg
        self.listing = ""
        self.file = "<stdin>"  # TODO

    def __str__(self):
        m = self.msg
        if '%s' in m:
            m = m % self.tok

        return "%s:%d:%d %s\n\n%s" % (
            self.file, self.pos[1], self.pos[0], m, self.listing)
