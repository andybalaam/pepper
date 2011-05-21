from abc import ABC

from libeeyore.values import *

@ABC
class EeyValue( object ):
	def __init__( self, env, const ):
		self.env = env
		self.const = const

	@abstractmethod
	def render( self ): pass

@ABC
def EeyVar( EeyValue ):
	def __init__( self, env, varname ):
		EeyValue.__init__( self, env, False )
		self.varname = varname

@ABC
def EeyInt( EeyValue ):
	def __init__( self, env, py_int ):
		EeyValue.__init__( self, env, True )
		self.value = py_int

@ABC
def EeyString( EeyValue ):
	def __init__( self, env, py_str ):
		EeyValue.__init__( self, env, True )
		self.value = py_str

