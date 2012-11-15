# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer
from libpepper.vals import *

def test_Add_known():
    env = PepEnvironment( PepCppRenderer() )
    value = PepPlus( PepInt( "14" ), PepInt( "17" ) )
    assert_equal( value.render( env ), "31" )

def test_Add_unknown():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["x"] = PepVariable( PepType( PepInt ), "x" )
    value = PepPlus( PepSymbol( "x" ), PepInt( "17" ) )
    assert_equal( value.render( env ), "(x + 17)" )

def test_Subtract_known():
    env = PepEnvironment( PepCppRenderer() )
    value = PepMinus( PepInt( "17" ), PepInt( "14" ) )
    assert_equal( value.render( env ), "3" )

def test_Subtract_unknown():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["x"] = PepVariable( PepType( PepInt ), "x" )
    value = PepMinus( PepSymbol( "x" ), PepInt( "17" ) )
    assert_equal( value.render( env ), "(x - 17)" )


def test_Multiply_known():
    env = PepEnvironment( PepCppRenderer() )
    value = PepTimes( PepInt( "4" ), PepInt( "3" ) )
    assert_equal( value.render( env ), "12" )

def test_Multiply_unknown():
    env = PepEnvironment( PepCppRenderer() )
    env.namespace["x"] = PepVariable( PepType( PepInt ), "x" )
    value = PepTimes( PepSymbol( "x" ), PepInt( "17" ) )
    assert_equal( value.render( env ), "(x * 17)" )

