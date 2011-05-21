
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.cppvalues import *
from libeeyore.cpprenderer import EeyCppRenderer

class NullRenderer:
	pass

def test_constintvalue():
	env = EeyEnvironment( NullRenderer() )
	value = EeyCppInt( env, "23" )

	assert_equal( value.render(), "23" )


def test_conststringvalue():
	env = EeyEnvironment( NullRenderer() )
	value = EeyCppString( env, "foo" )

	assert_equal( value.render(), '"foo"' )


