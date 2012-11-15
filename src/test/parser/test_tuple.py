# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result_from_code

def test_bracketed_number():
    assert_parser_result_from_code(
        r"""
print( ( 3 ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepInt('3'),
    )
)
""" )


def test_double_bracketed_number():
    assert_parser_result_from_code(
        r"""
print( ( ( 3 ) ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepInt('3'),
    )
)
""" )


def test_basic_tuple():
    assert_parser_result_from_code(
        r"""
print( ( 1, 2, 3 ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [COMMA:,]
        [INT:1]
        [INT:2]
        [INT:3]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepTuple(
            (
                PepInt('1'), 
                PepInt('2'), 
                PepInt('3')
            )
        ),
    )
)
""" )




