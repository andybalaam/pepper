from abc import ABCMeta
from abc import abstractmethod

class EeyValue( object ):
	__metaclass__ = ABCMeta

	def __init__( self, env, const ):
		self.env = env
		self.const = const

	@abstractmethod
	def render( self ):
		pass

class EeyVar( EeyValue ):

	def __init__( self, env, varname ):
		EeyValue.__init__( self, env, False )
		self.varname = varname

class EeyInt( EeyValue ):
	def __init__( self, env, py_int ):
		EeyValue.__init__( self, env, True )
		self.value = py_int

class EeyString( EeyValue ):

	def __init__( self, env, py_str ):
		EeyValue.__init__( self, env, True )
		self.value = py_str

