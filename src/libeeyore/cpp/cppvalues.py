
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
		value.left_value.render(), value.right_value.render() )

type2renderer = {
	EeyInt          : render_EeyInt,
	EeyPlus         : render_EeyPlus,
	EeyString       : render_EeyString,
	EeySymbol       : render_EeySymbol,
	EeyRuntimePrint : render_EeyRuntimePrint,
	}


