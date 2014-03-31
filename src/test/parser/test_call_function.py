# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result

def test_call_function():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(f)
0001:0002     LPAREN
0001:0003     RPAREN
0001:0004    NEWLINE
""",
        r"""
[LPAREN:]
    [SYMBOL:f]
[EOF:]
""",
        r"""
PepFunctionCall(
    PepSymbol('f'),
    ()
)
""" )


def test_call_function_with_args():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(f)
0001:0002     LPAREN
0001:0004        INT(1)
0001:0005      COMMA(,)
0001:0007        INT(2)
0001:0008      COMMA(,)
0001:0010        INT(3)
0001:0012     RPAREN
0001:0013    NEWLINE
""",
        r"""
[LPAREN:]
    [SYMBOL:f]
    [INT:1]
    [COMMA:,]
    [INT:2]
    [COMMA:,]
    [INT:3]
[EOF:]
""",
        r"""
PepFunctionCall(
    PepSymbol('f'),
    (
        PepInt('1'), 
        PepInt('2'), 
        PepInt('3')
    )
)
""" )

