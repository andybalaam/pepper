from pepper2like.ast.plaststring import plAstString
from pepper2like.characters import Characters
from pepper2like.type_check import type_check
from pepper2like.parser.plparsefailure import plParseFailure


def pl_parse(chars):
    type_check(Characters, chars)
    it = iter(chars)
    try:
        qu = next(it)
        if qu != '"':
            return plParseFailure()
    except StopIteration:
        return plParseFailure()
    ret = ""
    for c in it:
        if c == '"':
            return plAstString(ret)
        ret += c
    return plParseFailure()
