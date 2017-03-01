class pOpenBracket:
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s()" % (self.__class__.__name__)
