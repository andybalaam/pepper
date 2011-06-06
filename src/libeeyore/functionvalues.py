from abc import ABCMeta
from abc import abstractmethod
from itertools import izip

from environment import EeyEnvironment
from values import EeyValue
from values import all_known
from usererrorexception import EeyUserErrorException

def is_callable( value ):
	return True # TODO: check whether the object may be called

class EeyFunctionCall( EeyValue ):
	def __init__( self, func, args ):
		self.func = func
		self.args = args

	def evaluate( self, env ):
		if all_known( self.args, env ):
			fn = self.func.evaluate( env )
			assert is_callable( fn )
			return fn.call( env, self.args )
		else:
			return self


class EeyReturn( EeyValue ):
	def __init__( self, value ):
		self.value = value

	def evaluate( self, env ):
		return self.value.evaluate( env )

class EeyFunction( EeyValue ):
	__metaclass__ = ABCMeta

#	def __init__( self, arg_types_and_names ):
#		self.arg_types_and_names = arg_types_and_names

	@abstractmethod
	def call( self, env, args ): pass

	def is_known( self, env ):
		return True

class EeyUserFunction( EeyFunction ):
	def __init__( self, arg_types_and_names, body_stmts ):
		#EeyFunction.__init__( self, arg_types_and_names )
		self.arg_types_and_names = arg_types_and_names
		self.body_stmts = body_stmts

	def call( self, env, args ):
		if len( args ) != len( self.arg_types_and_names ):
			raise EeyUserErrorException(
				"Wrong number of arguments to function." )
			# TODO: function name
			# TODO: line, col, file

		for arg, (reqtype, reqname) in izip( args, self.arg_types_and_names ):
			if arg.__class__ is not reqtype:
				raise EeyUserErrorException(
					( "Incorrect argument type: '%s' should be a %s, but it "
					+ "is a %s" ) % ( reqname, reqtype, arg.__class__ ) )

		newenv = env.clone_deeper( args, self.arg_types_and_names )

		return self.body_stmts[0].evaluate( newenv )

