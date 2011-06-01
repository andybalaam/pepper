
from libeeyore.values import *
from libeeyore.builtins import *
from cppbuiltins import *

def render_EeySymbol( env, value ):
	return value.symbol_name

def render_EeyInt( env, value ):
	return str( value.value )

def render_EeyString( env, value ):
	return '"%s"' % value.value

def render_EeyPlus( env, value ):
	return "(%s + %s)" % (
		value.left_value.render( env ), value.right_value.render( env ) )

def render_EeyFunction( env, value ):
	raise Exception( "Don't know how to render a function yet" )

def render_EeyPrint( env, value ):
	return render_EeyFunction( env, value )

type2renderer = {
	EeyInt          : render_EeyInt,
	EeyPlus         : render_EeyPlus,
	EeyString       : render_EeyString,
	EeySymbol       : render_EeySymbol,
	EeyRuntimePrint : render_EeyRuntimePrint,
	EeyFunction     : render_EeyFunction,
	EeyPrint        : render_EeyPrint,
	}


