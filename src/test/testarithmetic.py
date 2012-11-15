# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper import builtins
from libpepper.environment import EeyEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import EeyCppRenderer
from libpepper.vals import *

def test_Add_known():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyPlus( EeyInt( "14" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "31" )

def test_Add_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["x"] = EeyVariable( EeyType( EeyInt ), "x" )
    value = EeyPlus( EeySymbol( "x" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "(x + 17)" )

def test_Subtract_known():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyMinus( EeyInt( "17" ), EeyInt( "14" ) )
    assert_equal( value.render( env ), "3" )

def test_Subtract_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["x"] = EeyVariable( EeyType( EeyInt ), "x" )
    value = EeyMinus( EeySymbol( "x" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "(x - 17)" )


def test_Multiply_known():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeyTimes( EeyInt( "4" ), EeyInt( "3" ) )
    assert_equal( value.render( env ), "12" )

def test_Multiply_unknown():
    env = EeyEnvironment( EeyCppRenderer() )
    env.namespace["x"] = EeyVariable( EeyType( EeyInt ), "x" )
    value = EeyTimes( EeySymbol( "x" ), EeyInt( "17" ) )
    assert_equal( value.render( env ), "(x * 17)" )

