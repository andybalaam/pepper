
from cppbuiltins import *
from libeeyore.builtins import *
from libeeyore.functionvalues import *
from libeeyore.values import *

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

def render_EeyDefine( env, value ):
	return ""

def render_EeyPass( env, value ):
	return ""


type2renderer = {
	EeyDefine       : render_EeyDefine,
	EeyFunction     : render_EeyFunction,
	EeyInt          : render_EeyInt,
	EeyPrint        : render_EeyPrint,
	EeyPass         : render_EeyPass,
	EeyRuntimePrint : render_EeyRuntimePrint,
	EeyPlus         : render_EeyPlus,
	EeyString       : render_EeyString,
	EeySymbol       : render_EeySymbol,
	}


