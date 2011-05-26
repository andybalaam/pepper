
from values import *

def render_EeySymbol( env, value ):
	#return evaluate().render()
	return None

def render_EeyInt( env, value ):
	return str( value.value )

def render_EeyString( env, value ):
	return '"%s"' % value.value

def render_EeyPlus( env, value ):
	return None
	#ans = value.evaluate()
	# TODO: check for None (i.e. non-const args)
	#return ans.render()

type2renderer = {
	EeyInt    : render_EeyInt,
	EeyString : render_EeyString,
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

