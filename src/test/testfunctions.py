
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer



@raises( EeyUserErrorException )
def test_Call_fn_with_wrong_num_args():
	env = EeyEnvironment( EeyCppRenderer() )

	fndecl = EeyDefine( EeySymbol( "myfunc" ),
		EeyUserFunction(
			"myfunc",
			EeyType( EeyInt ),
			(
				( EeyType( EeyInt ), EeySymbol( "x" ) ),
				),
			(
				EeyPass(),
				)
			)
		)

	assert_equal( fndecl.render( env ), "" )

	value = EeyFunctionCall( EeySymbol( "myfunc" ), () )

	value.render( env ) # should throw


@raises( EeyUserErrorException )
def test_Call_fn_with_wrong_arg_type():
	env = EeyEnvironment( EeyCppRenderer() )

	fndecl = EeyDefine( EeySymbol( "myfunc" ),
		EeyUserFunction(
			"myfunc",
			EeyType( EeyInt ),
			(
				( EeyType( EeyInt ), EeySymbol( "x" ) ),
				),
			(
				EeyPass(),
				)
			)
		)

	assert_equal( fndecl.render( env ), "" )

	value = EeyFunctionCall( EeySymbol( "myfunc" ), ( EeyString( "zzz" ), ) )

	value.render( env ) # should throw


def test_Define_and_call_fn_to_add_known_numbers():
	env = EeyEnvironment( EeyCppRenderer() )

	fndecl = EeyDefine( EeySymbol( "myfunc" ),
		EeyUserFunction(
			"myfunc",
			EeyType( EeyInt ),
			(
				( EeyType( EeyInt ), EeySymbol( "x" ) ),
				( EeyType( EeyInt ), EeySymbol( "y" ) )
				),
			(
				EeyReturn( EeyPlus( EeySymbol( "x" ), EeySymbol( "y" ) ) ),
				)
			)
		)

	assert_equal( fndecl.render( env ), "" )

	value = EeyFunctionCall( EeySymbol( "myfunc" ),
		( EeyInt( 3 ), EeyInt( 4 ) ) )

	assert_equal( value.render( env ), "7" )


def test_Define_and_call_fn_to_add_unknown_numbers():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["othernum"] = EeyVariable( EeyInt )

	fndecl = EeyDefine( EeySymbol( "myfunc" ),
		EeyUserFunction(
			"myfunc",
			EeyType( EeyInt ),
			(
				( EeyType( EeyInt ), EeySymbol( "x" ) ),
				( EeyType( EeyInt ), EeySymbol( "y" ) )
				),
			(
				EeyReturn( EeyPlus( EeySymbol( "x" ), EeySymbol( "y" ) ) ),
				)
			)
		)

	assert_equal( fndecl.render( env ), "" )

	value = EeyFunctionCall( EeySymbol( "myfunc" ),
		( EeyInt( 3 ), EeySymbol( "othernum" ) ) )

	assert_equal( value.render( env ), "myfunc( 3, othernum )" )
	assert_equal( env.renderer.functions[0],
"""int myfunc( int x, int y )
{
	return (x + y);
}
""" )


