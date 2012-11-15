# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cppvalues import *
from libpepper.cpp.cpprenderer import PepCppRenderer

def test_Int_evaluated_type():
    env = PepEnvironment( None )
    assert_equal( PepInt( '3' ).evaluated_type( env ), PepType( PepInt ) )

def test_Float_evaluated_type():
    env = PepEnvironment( None )
    assert_equal( PepFloat( '3.0' ).evaluated_type( env ), PepType( PepFloat ) )

def test_Bool_evaluated_type():
    env = PepEnvironment( None )
    assert_equal( PepBool( True ).evaluated_type( env ), PepType( PepBool ) )

def test_Variable_evaluated_type():
    env = PepEnvironment( None )
    assert_equal(
        PepVariable( PepType( PepString ), "x" ).evaluated_type( env ),
        PepType( PepString )
    )


def test_Plus_evaluated_type():
    env = PepEnvironment( None )
    plus = PepPlus( PepInt( "1" ), PepInt( "2" ) )
    assert_equal( plus.evaluated_type( env ), PepType( PepInt ) )


def test_Times_evaluated_type():
    env = PepEnvironment( None )
    times = PepTimes( PepInt( "1" ), PepInt( "2" ) )
    assert_equal( times.evaluated_type( env ), PepType( PepInt ) )



def test_Known_Symbol_evaluated_type():
    env = PepEnvironment( None )
    init = PepInit( PepType( PepBool ), PepSymbol( "x" ), PepBool( True ) )
    init.evaluate( env )

    assert_equal( PepSymbol( "x" ).evaluated_type( env ), PepType( PepBool ) )


def test_Unknown_Symbol_evaluated_type():
    env = PepEnvironment( None )
    init = PepInit( PepType( PepString ), PepSymbol( "x" ), PepVariable(
        PepType( PepString ), "x" ) )
    init.evaluate( env )

    assert_equal( PepSymbol( "x" ).evaluated_type( env ), PepType( PepString ) )



def test_FunctionCall_evaluated_type():
    env = PepEnvironment( None )
    func = PepUserFunction( "myfunc", PepType( PepBool ), (), ( PepPass(), ) )
    assert_equal(
        PepFunctionCall( func, () ).evaluated_type( env ),
        PepType( PepBool )
    )



def test_GreaterThan_evaluated_type():
    env = PepEnvironment( None )
    value = PepGreaterThan( PepInt( "4" ), PepInt( "5" ) )
    assert_equal( value.evaluated_type( env ), PepType( PepBool ) )





