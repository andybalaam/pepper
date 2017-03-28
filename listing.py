from type_check import type_check
from pltypes.pltuple import plTuple


def _lines(num_width, first_line, lines):
    return [
        ("%%%dd|%%s" % num_width) % (i, l)
        for i, l in enumerate(lines, first_line)
    ]


def _here_line(num_width, column):
    return (" " * (num_width + column)) + "^^^ <--- here"


def _split_lines(before_str, after_str):
    before = before_str.split("\n")
    after = after_str.split("\n")

    # Stick the first line of after onto the end
    # of before if before does not end with \n
    if before[-1] == "":
        before = before[:-1]
    else:
        if len(after) > 0:
            before[-1] += after[0]
            after = after[1:]

    if len(after) > 0 and after[-1] == "":
        after = after[:-1]

    return before, after


def listing(before_str, after_str, pos):
    type_check(str, before_str, "before_str")
    type_check(str, after_str, "after_str")
    type_check(plTuple(size=2, type_=int), pos, "pos")

    before, after = _split_lines(before_str, after_str)
    column, row = pos

    # The largest line number will be row + len(after)
    num_width = len("%d" % (row + len(after)))

    return "\n".join(
        _lines(num_width, 1 + row - len(before), before) +
        [_here_line(num_width, column)] +
        _lines(num_width, 1 + row, after)
    ) + "\n"
