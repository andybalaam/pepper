from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Hello_World():
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( env )

	value = EeyFunctionCall( EeySymbol( "print" ),
		( EeyString( "Hello, World!" ), ) )

	assert_equal( env.render_exe( ( value, ) ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
	printf( "Hello, World!\\n" );

	return 0;
}
""" )

def test_Echo_arg1():
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( env )

	# import sys
	#
	# def string getname( string name ):
	#     return name
	#
	# print sys.argv[1]

	impt = EeyImport( "sys" )

#	fndef = EeyDefine( EeySymbol( "getname" ),
#		EeyUserFunction(
#			EeyType( EeyString ),
#			(
#				( EeyType( EeyString ), EeySymbol( "name" ) ),
#				),
#			(
#				EeyReturn( EeySymbol( "name" ) ),
#				)
#			)
#		)

	fncall = EeyFunctionCall( EeySymbol( "print" ),
		( EeyArrayLookup( EeySymbol( "sys.argv" ), EeyInt( 1 ) ), ) )

	program = ( impt, fncall )

	assert_equal( env.render_exe( program ), """#include <stdio.h>

int main( int argc, char* argv[] )
{
	printf( "%s\\n", argv[1] );

	return 0;
}
""" )

