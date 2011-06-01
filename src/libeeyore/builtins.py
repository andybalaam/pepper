from abc import ABCMeta
from abc import abstractmethod

from values import EeyValue

class EeyFunction( EeyValue ):
	__metaclass__ = ABCMeta

	@abstractmethod
	def call( self, args ): pass

	def is_const( self, env ):
		return True

# --------

class EeyRuntimePrint( EeyValue ):
	def __init__( self, args ):
		self.args = args

class EeyPrint( EeyFunction ):

	def call( self, args ):
		return EeyRuntimePrint( args )


def add_builtins( env ):
	env.namespace["print"] = EeyPrint()
