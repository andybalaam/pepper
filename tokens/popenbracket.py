from tokens.ptoken import pToken


class pOpenBracket(pToken):
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)

    def __eq__(self, other):
        return type(self) == type(other)
