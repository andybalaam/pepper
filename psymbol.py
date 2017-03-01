class pSymbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.name == other.name
        )

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.name)
