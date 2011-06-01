
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

def test_Const_int_value_renders_as_a_number():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyInt( "23" )

	assert_equal( value.render( env ), "23" )


def test_Const_string_value_renders_as_a_string():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyString( "foo" )

	assert_equal( value.render( env ), '"foo"' )


def test_Variable_referring_to_known_int_renders_like_an_int():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["myvariable"] = EeyInt( 23 )

	value = EeySymbol( "myvariable" )

	assert_equal( value.render( env ), "23" )

def test_Add_two_known_ints_renders_calculated_sum():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyPlus( EeyInt( 2 ), EeyInt( 3 ) )

	assert_equal( value.render( env ), "5" )

def test_Nonconst_variable_renders_as_symbol():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["myvariable"] = EeyVariable( EeyInt )

	value = EeySymbol( "myvariable" )

	assert_equal( value.render( env ), "myvariable" )

def test_Add_Nonconst_to_known_literal_renders_uncalculated_sum():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["input"] = EeyVariable( EeyInt )

	value = EeyPlus( EeyInt( 4 ), EeySymbol( "input" ) )

	assert_equal( value.render( env ), "(4 + input)" )

def test_Add_Nonconst_to_known_symbol_renders_uncalculated_sum():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["input"] = EeyVariable( EeyInt )
	env.namespace["four"] = EeyInt( 4 )

	value = EeyPlus( EeySymbol( "input" ), EeySymbol( "four" ) )

	assert_equal( value.render( env ), "(input + 4)" )


def test_Nonconst_inside_nested_plus_causes_whole_sum_to_be_uncalculated():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["input"] = EeyVariable( EeyInt )

	value = EeyPlus( EeyInt( 4 ),
		EeyPlus( EeyInt( 5 ), EeySymbol( "input" ) ) )

	assert_equal( value.render( env ), "(4 + (5 + input))" )


def test_Print_string_renders_as_printf():
	env = EeyEnvironment( EeyCppRenderer() )

	value = EeyFunctionCall( EeySymbol( "print" ),
		( EeyString( "hello" ), ) )

	assert_equal( value.render( env ), 'printf( "hello\n" )' )
	assert_equal( env.renderer.headers, [ "stdio.h" ] )

