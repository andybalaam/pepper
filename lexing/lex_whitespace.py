from type_check import type_check
from pltypes.peekable import Peekable
from pltypes.plchar import plChar
from pwhitespace import pWhitespace


def _is_whitespace(char):
    type_check(plChar(), char, "char")
    return char in " \n"


def lex_whitespace(chars):
    type_check(Peekable(), chars, "chars")
    ret = ""
    try:
        while _is_whitespace(chars.peek()):
            ret += str(next(chars))
    except StopIteration as e:
        if len(ret) > 0:
            return pWhitespace(value=ret)
        else:
            raise e
    if len(ret) > 0:
        return pWhitespace(value=ret)
    else:
        return None
