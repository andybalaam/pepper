
from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Add_known():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyPlus( EeyInt( "14" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "31" )

def test_Add_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["x"] = EeyVariable( EeyInt )
    value = EeyPlus( EeySymbol( "x" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "(x + 17)" )

def test_Multiply_known():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyTimes( EeyInt( "4" ), EeyInt( "3" ) )
    assert_equal( value.render( env ), "12" )

def test_Multiply_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["x"] = EeyVariable( EeyInt )
    value = EeyTimes( EeySymbol( "x" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "(x * 17)" )

