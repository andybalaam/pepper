# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper.environment import PepEnvironment
from libpepper.vals.all_values import *

from assert_parser_result import assert_parser_result_from_code

def Bracketed_number_is_not_a_tuple__test():
    assert_parser_result_from_code(
        r"""
print( ( 3 ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
[EOF:]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepInt('3'),
    )
)
""" )


def Double_bracketed_number_is_not_a_tuple__test():
    assert_parser_result_from_code(
        r"""
print( ( ( 3 ) ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
[EOF:]
""",
        r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepInt('3'),
    )
)
""" )


def Comma_separated_bracketed_expression_is_a_tuple__test():
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
[EOF:]
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


def Evaluating_a_tuple_evaluates_items__test():
    env = PepEnvironment( None )

    tup = PepTuple(
        (
            PepPlus( PepInt( 1 ), PepInt( 2 ) ),
            PepPlus( PepInt( 4 ), PepInt( 1 ) ),
        )
    )

    # Sanity
    assert_equals( PepPlus, tup.items[0].__class__ )
    assert_equals( PepPlus, tup.items[1].__class__ )

    # This is what we are testing
    evald_tup = tup.evaluate( env )

    # The items inside the tuple were evaluated
    assert_equals( PepInt, evald_tup.items[0].__class__ )
    assert_equals( PepInt, evald_tup.items[1].__class__ )
    assert_equals( "3", evald_tup.items[0].value )


