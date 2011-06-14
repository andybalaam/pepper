
from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer
from libeeyore.builtinmodules.eeysys import EeySysArgv


#def test_Known_plus_string():
#	env = EeyEnvironment( EeyCppRenderer() )
#	env.namespace["input"] = EeyVariable( EeyString )
#
#	value = EeyPlus( EeyString( "known" ), EeySymbol( "input" ) )
#
#	assert_equal( value.render( env ), '("known" + input)' )
#
#
#def test_Known_plus_string_inside_print():
#	env = EeyEnvironment( EeyCppRenderer() )
#	env.namespace["input"] = EeyVariable( EeyString )
#
#	value = EeyPrint( EeyPlus( EeyString( "known" ), EeySymbol( "input" ) ) )
#
#	assert_equal( value.render( env ), 'printf( "known%s", input )' )

def test_Known_plus_argv():
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( env )

	value = EeyFunctionCall( EeySymbol( "print" ), (
		EeyPlus(
			EeyString( "known" ),
			EeyArrayLookup( EeySysArgv(), EeyInt( 1 ) )
			),
		) )

	assert_equal( value.render( env ), 'printf( "known%s\\n", argv[1] )' )


def test_Known_plus_argv_plus_known():
	env = EeyEnvironment( EeyCppRenderer() )
	builtins.add_builtins( env )

	value = EeyFunctionCall( EeySymbol( "print" ), (
		EeyPlus(
			EeyString( "known" ),
			EeyPlus(
				EeyArrayLookup( EeySysArgv(), EeyInt( 1 ) ),
				EeyString( "known2" )
				)
			),
		) )

	assert_equal( value.render( env ), 'printf( "known%sknown2\\n", argv[1] )' )


