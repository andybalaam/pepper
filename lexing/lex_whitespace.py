from charatpostype import CharAtPosType
from lexing.lexfailure import LexFailure
from type_check import type_check
from pltypes.peekable import Peekable
from tokens.pwhitespace import pWhitespace


def _is_whitespace(char, chars):
    type_check(CharAtPosType(), char, "char")
    if char.char == "\t":
        raise LexFailure(chars, "Tab characters are not allowed.")
    return char.char in " \n"


def lex_whitespace(chars):
    type_check(Peekable(), chars, "chars")
    ret = ""
    try:
        while _is_whitespace(chars.peek(), chars):
            ret += next(chars).char
    except StopIteration as e:
        if len(ret) > 0:
            return pWhitespace(value=ret)
        else:
            raise e
    if len(ret) > 0:
        return pWhitespace(value=ret)
    else:
        return None
