from pclosebracket import pCloseBracket
from popenbracket import pOpenBracket


def lex_punctuation(chars):
    ch = next(chars)
    if ch == "(":
        return pOpenBracket()
    elif ch == ")":
        return pCloseBracket()
    else:
        return None
