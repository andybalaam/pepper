# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result

def test_operator_plus():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(a)
0001:0002       PLUS(+)
0001:0003     SYMBOL(b)
0001:0004    NEWLINE
""",
        r"""
[PLUS:+]
    [SYMBOL:a]
    [SYMBOL:b]
[EOF:]
""",
        r"""
PepPlus(
    PepSymbol('a'),
    PepSymbol('b')
)
""" )

def test_operator_minus():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(a)
0001:0002      MINUS(-)
0001:0003     SYMBOL(b)
0001:0004    NEWLINE
""",
        r"""
[MINUS:-]
    [SYMBOL:a]
    [SYMBOL:b]
[EOF:]
""",
        r"""
PepMinus(
    PepSymbol('a'),
    PepSymbol('b')
)
""" )

def test_operator_times():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(a)
0001:0002      TIMES(*)
0001:0003     SYMBOL(b)
0001:0004    NEWLINE
""",
        r"""
[TIMES:*]
    [SYMBOL:a]
    [SYMBOL:b]
[EOF:]
""",
        r"""
PepTimes(
    PepSymbol('a'),
    PepSymbol('b')
)
""" )


def test_operator_greater_than():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(a)
0001:0002         GT(>)
0001:0003     SYMBOL(b)
0001:0004    NEWLINE
""",
        r"""
[GT:>]
    [SYMBOL:a]
    [SYMBOL:b]
[EOF:]
""",
        r"""
PepGreaterThan(
    PepSymbol('a'),
    PepSymbol('b')
)
""" )


def test_plus_in_function_call():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(print)
0001:0006     LPAREN
0001:0008        INT(3)
0001:0010       PLUS(+)
0001:0012     SYMBOL(b)
0001:0014     RPAREN
0001:0015    NEWLINE
""",
        r"""
[LPAREN:]
    [SYMBOL:print]
    [PLUS:+]
        [INT:3]
        [SYMBOL:b]
[EOF:]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepPlus(
            PepInt('3'),
            PepSymbol('b')
        ),
    )
)
""" )


