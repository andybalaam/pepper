
from libeeyore.values import *

class EeyCppVar( EeyVar ):
	def render( self ):
		return self.varname

def evar( env, varname ):
	return EeyCppVar( env, varname )

class EeyCppInt( EeyInt ):
	def render( self ):
		return str( self.value )

def eint( env, strint ):
	return EeyCppInt( env, int( strint ) )

class EeyCppString( EeyString ):
	def render( self ):
		return self.value

def estring( env, strvalue ):
	return EeyCppString( env, strvalue )

