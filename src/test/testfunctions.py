
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer



#@throws( EeyTypeError )
#def test_Call_fn_with_wrong_arg_type():
#	env = EeyEnvironment( EeyCppRenderer() )
#
#	fndecl = EeyDefine( EeySymbol( "myfunc" ),
#		EeyFunction(
#			(
#				( EeyInt, EeySymbol( "x" ) ),
#				),
#			(
#				EeyPass(),
#				)
#			)
#		)
#
#	assert_equal( fndecl.render( env ), "" )
#
#	value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "zzz" ), ) )
#
#	value.render( env ) # should throw


#def test_Define_and_call_fn_to_add_known_numbers():
#	env = EeyEnvironment( EeyCppRenderer() )
#
#	fndecl = EeyDefine( EeySymbol( "myfunc" ),
#		EeyFunction(
#			(
#				( EeyInt, EeySymbol( "x" ) ),
#				( EeyInt, EeySymbol( "y" ) )
#				),
#			(
#				EeyReturn( EeyPlus( EeySymbol( "x" ), EeySymbol( "y" ) ) ),
#				)
#			)
#		)
#
#	assert_equal( fndecl.render( env ), "" )
#
#	value = EeyFunctionCall( EeySymbol( "myfunc" ),
#		( EeyInt( 3 ), EeyInt( 4 ) ) )
#
#	assert_equal( value.render( env ), "7" )
#
