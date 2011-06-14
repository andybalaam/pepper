from abc import ABCMeta
from abc import abstractmethod
from itertools import izip

from environment import EeyEnvironment
from values import EeySymbol
from values import EeyValue
from values import EeyVariable
from values import all_known
from usererrorexception import EeyUserErrorException

def is_callable( value ):
	return True # TODO: check whether the object may be called

class EeyFunctionCall( EeyValue ):
	def __init__( self, func, args ):
		assert( func.__class__ == EeySymbol ) # TODO: Might not be?  Handle
		                                      #       expressions that eval to
		                                      #       a symbol?
		self.func_name = func.symbol_name
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


class EeyRuntimeUserFunction( EeyValue ):
	def __init__( self, user_function, args ):
		# TODO: check arg types
		self.user_function = user_function
		self.args = args


class EeyUserFunction( EeyFunction ):
	def __init__( self, name, ret_type, arg_types_and_names, body_stmts ):
		#EeyFunction.__init__( self, arg_types_and_names )
		self.name = name
		self.ret_type = ret_type
		self.arg_types_and_names = arg_types_and_names
		self.body_stmts = body_stmts

	def call( self, env, args ):
		if all_known( args, env ):
			if len( args ) != len( self.arg_types_and_names ):
				raise EeyUserErrorException(
					"Wrong number of arguments to function." )
				# TODO: function name
				# TODO: line, col, file

			for arg, (reqtype, reqname) in izip( args,
					self.arg_types_and_names ):
				#while arg.__class__
				if arg.__class__ is not reqtype.value:
					raise EeyUserErrorException(
						( "Incorrect argument type: '%s' should be a %s, but "
							+ "it is a %s" ) % (
							reqname.symbol_name, reqtype.value,
							arg.__class__
							)
						)

			newenv = self.execution_environment( env, args, True )

			# TODO: not just the first statement
			return self.body_stmts[0].evaluate( newenv )
		else:
			return EeyRuntimeUserFunction( self, args )

	def execution_environment( self, env, args, known ):
		newenv = env.clone_deeper()

		for val, (tp, name) in izip( args, self.arg_types_and_names ):
			if known:
				val = val.evaluate( env )
			else:
				val = EeyVariable( tp.value )
			newenv.namespace[name.name()] = val

		return newenv

