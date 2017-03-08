import re
from psymbol import pSymbol

begin_symbol_char_re_ = re.compile("[a-zA-Z_]")
symbol_char_re_ = re.compile("[a-zA-Z0-9_]")


def lex_symbol(chars):
    ch = chars.peek()
    if not begin_symbol_char_re_.match(ch):
        return None

    ret = ""
    while True:
        try:
            ch = chars.peek()
        except StopIteration as e:
            if len(ret) > 0:
                return pSymbol(ret)
            else:
                raise e

        if symbol_char_re_.match(ch):
            ret += next(chars)
        else:
            return pSymbol(ret)
