# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from libeeyore.functionvalues import *
from libeeyore.languagevalues import *
from libeeyore.values import *

from libeeyore.quotevalues import EeyQuote

def test_evaluate_returns_same_with_no_symbol_lookup():
    env = EeyEnvironment( EeyCppRenderer() )
    stmt = EeyQuote( ( EeySymbol('a'), ) )
    assert_true( stmt.evaluate( env ) is stmt )


def test_can_unquote_and_get_value_out():
    env = EeyEnvironment( EeyCppRenderer() )
    stmt = EeyQuote( ( EeyInt('98'), ) )

    execd_stmt = stmt.unquote().evaluate( env )

    assert_equal( EeyInt, type( execd_stmt ) )
    assert_equal( '98', execd_stmt.value  )


def test_evaluate_method_call_unquotes():
    env = EeyEnvironment( EeyCppRenderer() )
    add_builtins( env )

    # code mycode = quote:
    #     98
    quoting_stmt = EeyInit(
        EeySymbol('code'),
        EeySymbol('mycode'),
        EeyQuote(
            ( EeyInt('98'), )
        )
    )

    # mycode.evaluate()
    unquoting_stmt = EeyFunctionCall( EeySymbol( "mycode.evaluate" ), () )

    quoting_stmt.evaluate( env )
    ans = unquoting_stmt.evaluate( env )

    assert_equal( EeyInt, type( ans ) )
    assert_equal( '98', ans.value  )


