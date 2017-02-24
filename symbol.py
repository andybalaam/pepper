class Symbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.name == other.name
        )
