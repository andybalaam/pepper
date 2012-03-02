
from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Int_evaluated_type():
    env = EeyEnvironment( None )
    assert_equal( EeyInt( '3' ).evaluated_type( env ), EeyInt )

def test_Float_evaluated_type():
    env = EeyEnvironment( None )
    assert_equal( EeyFloat( '3.0' ).evaluated_type( env ), EeyFloat )

def test_Bool_evaluated_type():
    env = EeyEnvironment( None )
    assert_equal( EeyBool( True ).evaluated_type( env ), EeyBool )

def test_Variable_evaluated_type():
    env = EeyEnvironment( None )
    assert_equal( EeyVariable( EeyString ).evaluated_type( env ), EeyString )


def test_Plus_evaluated_type():
    env = EeyEnvironment( None )
    plus = EeyPlus( EeyInt( "1" ), EeyInt( "2" ) )
    assert_equal( plus.evaluated_type( env ), EeyInt )


def test_Times_evaluated_type():
    env = EeyEnvironment( None )
    times = EeyTimes( EeyInt( "1" ), EeyInt( "2" ) )
    assert_equal( times.evaluated_type( env ), EeyInt )



def test_Known_Symbol_evaluated_type():
    env = EeyEnvironment( None )
    init = EeyInit( EeyType( EeyBool ), EeySymbol( "x" ), EeyBool( True ) )
    init.evaluate( env )

    assert_equal( EeySymbol( "x" ).evaluated_type( env ), EeyBool )


def test_Unknown_Symbol_evaluated_type():
    env = EeyEnvironment( None )
    init = EeyInit( EeyType( EeyString ), EeySymbol( "x" ), EeyVariable(
        EeyString ) )
    init.evaluate( env )

    assert_equal( EeySymbol( "x" ).evaluated_type( env ), EeyString )



def test_FunctionCall_evaluated_type():
    env = EeyEnvironment( None )
    func = EeyUserFunction( "myfunc", EeyType( EeyBool ), (), ( EeyPass(), ) )
    assert_equal( EeyFunctionCall( func, () ).evaluated_type( env ),
        EeyBool )



def test_GreaterThan_evaluated_type():
    env = EeyEnvironment( None )
    value = EeyGreaterThan( EeyInt( "4" ), EeyInt( "5" ) )
    assert_equal( value.evaluated_type( env ), EeyBool )





