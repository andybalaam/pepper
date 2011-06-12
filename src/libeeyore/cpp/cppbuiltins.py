
from libeeyore.eeyinterface import implements_interface
from libeeyore.values import *

def render_EeyRuntimePrint( env, value ):
	assert( len( value.args ) == 1 ) # TODO: not an assert
	arg0 = value.args[0]
	#assert( arg0.__class__ is EeyString ) # TODO: not assert, less specific?

	env.renderer.headers.append( "stdio.h" )

	arg0 = arg0.evaluate( env )

	if arg0.__class__ is EeyString:
		# We don't call render, because we add our own quotes here
		fmtstr = '"%s\\n"' % arg0.as_py_str()
		fmtarg = None
	elif arg0.__class__ is EeyInt:
		fmtstr = '"%d\\n"'
		fmtarg = arg0.render( env )
	elif implements_interface( arg0, EeyString ):
		fmtstr = '"%s\\n"'
		fmtarg = arg0.render( env )
	else:
		raise Exception( "Unknown argument type to print: "
			+ str( arg0.__class__ ) )

	ret = 'printf( ' + fmtstr
	if fmtarg is not None:
		ret += ", "
		ret += fmtarg
	ret += " )"

	return ret

