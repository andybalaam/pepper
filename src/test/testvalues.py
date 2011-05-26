
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cppvalues import *
from libeeyore.cpprenderer import EeyCppRenderer

def test_Const_int_value_renders_as_a_number():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyInt( env, render_EeyInt, "23" )

	assert_equal( value.render(), "23" )


def test_Const_string_value_renders_as_a_string():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyString( env, render_EeyString, "foo" )

	assert_equal( value.render(), '"foo"' )


def test_Variable_referring_to_const_int_renders_like_an_int():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["myvariable"] = EeyInt( env, render_EeyInt, 23 )

	value = EeySymbol( env, render_EeySymbol, "myvariable" )

	assert_equal( value.render(), "23" )

def test_Add_two_const_ints_renders_as_sum():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyPlus( env, render_EeyPlus,
		EeyInt( env, render_EeyInt, 2 ), EeyInt( env, render_EeyInt, 3 ) )

	assert_equal( value.render(), "5" )

