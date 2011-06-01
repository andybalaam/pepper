from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Hello_World():
	env = EeyEnvironment( EeyCppRenderer() )

	value = EeyFunctionCall( EeySymbol( "print" ),
		( EeyString( "Hello, World!" ), ) )

	assert_equal( env.render_exe( ( value, ) ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
	printf( "Hello, World!\\n" );

	return 0;
}
""" )

