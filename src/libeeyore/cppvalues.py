
from values import *

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
	EeyInt    : render_EeyInt,
	EeyPlus   : render_EeyPlus,
	EeyString : render_EeyString,
	EeySymbol : render_EeySymbol,
	}

#class EeyCppSymbol( EeyRenderer ):
#	def __init__( self, value ):
#		self.value = value
#
#	def render( self ):
#		return self.value.lookup().render()
#
#class EeyCppInt( EeyRenderer ):
#	def render( self ):
#		return str( self.value.value )
#
#class EeyCppString( EeyRenderer ):
#	def render( self ):
#		return '"%s"' % self.value.value
#
#
#class EeyCppPlus( EeyRenderer ):
#	def render( self ):
#		ans = self.value.calculate()
#		if ans is not None:
#			return ans.render()
#		else:
#			return "(%s + %s)" % (
#				self.left_value.render(),
#				self.right_value.render() )
#

