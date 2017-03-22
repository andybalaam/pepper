from type_check import type_check
from pltypes.plchar import plChar


class CharAtPos:
    def __init__(self, char, column, line):
        type_check(plChar(), char, "char")
        type_check(int, column, "column")
        type_check(int, line, "line")

        self.char = char
        self.pos = (column, line)
