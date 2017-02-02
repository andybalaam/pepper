# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Bear with me while I speak, and after I have spoken, mock on.
# Job 21 v3

from nose.tools import *

from assert_parser_result import assert_parser_result_from_code

def Basic_while_loop__test():
    assert_parser_result_from_code(
        r"""
int a = 0
while a > 5:
    pass
""",
        r"""
[EQUALS:=]
    [SYMBOL:int]
    [SYMBOL:a]
    [INT:0]
["while":while]
    [GT:>]
        [SYMBOL:a]
        [INT:5]
    [COLON::]
        [SYMBOL:pass]
[EOF:]
""",
        r"""
PepInit(
    PepSymbol('int'),
    PepSymbol('a'),
    PepInt('0')
)
PepWhile(
    PepGreaterThan(
        PepSymbol('a'),
        PepInt('5')
    ),
    (
        PepSymbol('pass'),
    )
)
""" )


