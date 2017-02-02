# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result_from_code

def test_for_in_tuple():
    assert_parser_result_from_code(
        r"""
for int i in ( 1, 2, 3 ):
    pass
""",
        r"""
["for":for]
    [SYMBOL:int]
    [SYMBOL:i]
    [COMMA:,]
        [INT:1]
        [INT:2]
        [INT:3]
    [COLON::]
        [SYMBOL:pass]
[EOF:]
""",
        r"""
PepFor(
    PepSymbol('int'),
    PepSymbol('i'),
    PepTuple(
        (
            PepInt('1'), 
            PepInt('2'), 
            PepInt('3')
        )
    ),
    (
        PepSymbol('pass'),
    )
)
""" )


def test_for_int_in_range():
    assert_parser_result_from_code(
        r"""
for int i in range( 0, 4 ):
    print( i )
""",
        r"""
["for":for]
    [SYMBOL:int]
    [SYMBOL:i]
    [LPAREN:(]
        [SYMBOL:range]
        [INT:0]
        [COMMA:,]
        [INT:4]
    [COLON::]
        [LPAREN:(]
            [SYMBOL:print]
            [SYMBOL:i]
[EOF:]
""",
        r"""
PepFor(
    PepSymbol('int'),
    PepSymbol('i'),
    PepFunctionCall(
        PepSymbol('range'),
        (
            PepInt('0'), 
            PepInt('4')
        )
    ),
    (
        PepFunctionCall(
            PepSymbol('print'),
            (
                PepSymbol('i'),
            )
        ),
    )
)
""" )


def test_comments_in_for():
    assert_parser_result_from_code(
        r"""
for int i in range( 0, 4 ):
    # ignored
    print( i )
# ignored
""",
        r"""
["for":for]
    [SYMBOL:int]
    [SYMBOL:i]
    [LPAREN:(]
        [SYMBOL:range]
        [INT:0]
        [COMMA:,]
        [INT:4]
    [COLON::]
        [LPAREN:(]
            [SYMBOL:print]
            [SYMBOL:i]
[EOF:]
""",
        r"""
PepFor(
    PepSymbol('int'),
    PepSymbol('i'),
    PepFunctionCall(
        PepSymbol('range'),
        (
            PepInt('0'), 
            PepInt('4')
        )
    ),
    (
        PepFunctionCall(
            PepSymbol('print'),
            (
                PepSymbol('i'),
            )
        ),
    )
)
""" )


