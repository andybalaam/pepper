from abc import ABC

@ABC
class EeyRenderer( object ):
	@abstractmethod
	def render_var( self, varname ): pass

class EeyCppRenderer( EeyRenderer ):

	def render_var( self, varname ):
		return varname

	def render_int( self, pyint ):
		return str(  pyint )

	def render_string( self, pystr ):
		return pystr

	def render_string_concat( self ):


class EeyEnvironment( object ):
	pass

def is_const( value ):
	return value.const

def EeyString( EeyValue ):
	def __init__( 


