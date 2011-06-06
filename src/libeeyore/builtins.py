from abc import ABCMeta
from abc import abstractmethod

from values import EeyValue

class EeyFunction( EeyValue ):
	__metaclass__ = ABCMeta

#	def __init__( self, arg_types_and_names ):
#		self.arg_types_and_names = arg_types_and_names

	@abstractmethod
	def call( self, args ): pass

	def is_known( self, env ):
		return True

# --------

class EeyRuntimePrint( EeyValue ):
	def __init__( self, args ):
		self.args = args

class EeyPrint( EeyFunction ):

#	def __init__( self ):
#		EeyFunction.__init__( self, ( ( EeyAny, EeySymbol( "object" ) ), ) )

	def call( self, args ):
		return EeyRuntimePrint( args )


def add_builtins( env ):
	env.namespace["print"] = EeyPrint()
