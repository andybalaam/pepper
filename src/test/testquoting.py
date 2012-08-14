from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer
from libeeyore.values import *
from libeeyore.quotevalues import EeyQuote

def test_evaluate_returns_same_with_no_symbol_lookup():
    env = EeyEnvironment( EeyCppRenderer() )
    stmt = EeyQuote( ( EeySymbol('a'), ) )
    assert_true( stmt.evaluate( env ) is stmt )


def test_can_execute_and_get_value_out():
    env = EeyEnvironment( EeyCppRenderer() )
    stmt = EeyQuote( ( EeyInt('98'), ) )

    execd_stmt = stmt.execute().evaluate( env )

    assert_equal( EeyInt, type( execd_stmt ) )
    assert_equal( '98', execd_stmt.value  )

