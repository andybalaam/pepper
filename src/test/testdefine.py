
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.usererrorexception import EeyUserErrorException
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Define_and_use_int():
    env = EeyEnvironment( EeyCppRenderer() )

    defstmt = EeyDefine( EeySymbol( "mynum" ), EeyInt( 12 ) )

    assert_equal( defstmt.render( env ), "" )

    value = EeySymbol( "mynum" )

    assert_equal( value.render( env ), "12" )


@raises( EeyUserErrorException )
def test_Use_an_undefined_symbol_throws():
    env = EeyEnvironment( EeyCppRenderer() )
    value = EeySymbol( "mynotdef" )
    value.render( env ) # Should throw


@raises( EeyUserErrorException )
def test_Defining_a_symbol_twice_fails():
    env = EeyEnvironment( EeyCppRenderer() )
    defstmt1 = EeyDefine( EeySymbol( "mynum" ), EeyInt( 12 ) )
    defstmt2 = EeyDefine( EeySymbol( "mynum" ), EeyInt( 13 ) )
    defstmt1.render( env )
    defstmt2.render( env ) # Should throw

