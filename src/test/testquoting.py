# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper.builtins import add_builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.functionvalues import *
from libpepper.languagevalues import *
from libpepper.values import *

from libpepper.quotevalues import PepQuote

def test_evaluate_returns_same_with_no_symbol_lookup():
    env = PepEnvironment( PepCppRenderer() )
    stmt = PepQuote( ( PepSymbol('a'), ) )
    assert_true( stmt.evaluate( env ) is stmt )


def test_can_unquote_and_get_value_out():
    env = PepEnvironment( PepCppRenderer() )
    stmt = PepQuote( ( PepInt('98'), ) )

    execd_stmt = stmt.unquote().evaluate( env )

    assert_equal( PepInt, type( execd_stmt ) )
    assert_equal( '98', execd_stmt.value  )


def test_evaluate_method_call_unquotes():
    env = PepEnvironment( PepCppRenderer() )
    add_builtins( env )

    # code mycode = quote:
    #     98
    quoting_stmt = PepInit(
        PepSymbol('code'),
        PepSymbol('mycode'),
        PepQuote(
            ( PepInt('98'), )
        )
    )

    # mycode.evaluate()
    unquoting_stmt = PepFunctionCall( PepSymbol( "mycode.evaluate" ), () )

    quoting_stmt.evaluate( env )
    ans = unquoting_stmt.evaluate( env )

    assert_equal( PepInt, type( ans ) )
    assert_equal( '98', ans.value  )


