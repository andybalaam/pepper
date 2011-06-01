
from libeeyore.values import *

def render_EeyRuntimePrint( env, value ):
	assert( len( value.args ) == 1 ) # TODO: not an assert
	arg0 = value.args[0]
	assert( arg0.__class__ is EeyString ) # TODO: not assert, less specific?

	env.renderer.headers.append( "stdio.h" )

	return 'printf( "%s\n" )' % arg0.as_py_str()

