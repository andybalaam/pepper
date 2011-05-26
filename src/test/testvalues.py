
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cppvalues import *
from libeeyore.cpprenderer import EeyCppRenderer

def test_Const_int_value_renders_as_a_number():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyInt( env, "23" )

	assert_equal( value.render(), "23" )


def test_Const_string_value_renders_as_a_string():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyString( env, "foo" )

	assert_equal( value.render(), '"foo"' )


def test_Variable_referring_to_const_int_renders_like_an_int():
	env = EeyEnvironment( EeyCppRenderer() )
	env.namespace["myvariable"] = EeyInt( env, 23 )

	value = EeySymbol( env, "myvariable" )

	assert_equal( value.render(), "23" )

def test_Add_two_const_ints_renders_as_sum():
	env = EeyEnvironment( EeyCppRenderer() )
	value = EeyPlus( env, EeyInt( env, 2 ), EeyInt( env, 3 ) )

	assert_equal( value.render(), "5" )

#def test_Nonconst_variable_renders_as_symbol():
#	env = EeyEnvironment( EeyCppRenderer() )
#	
#


