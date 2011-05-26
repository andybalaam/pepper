from abc import ABCMeta
from abc import abstractmethod

#class EeyRenderer( object ):
#	__metaclass__ = ABCMeta
#
#	def __init__( self, env, value ):
#		self.env = env
#		self.value = value
#
#	@abstractmethod
#	def render( self ):
#		pass

class EeyValue( object ):
	def __init__( self, env, renderer ):
		self.env = env
		self.renderer = renderer

	def render( self ):
#		ev = self
#		oldev = None
#		while ev is not oldev:
#			oldev = ev
#			ev = ev.evaluate()

		ev = self.evaluate()
		return self.env.render_value( ev )

class EeySymbol( EeyValue ):
	def __init__( self, env, renderer, symbol_name ):
		EeyValue.__init__( self, env, renderer )
		self.symbol_name = symbol_name

	def evaluate( self ):
		assert( self.symbol_name in self.env.namespace ) # TODO: not an assert
		return self.env.namespace[self.symbol_name]


class EeyInt( EeyValue ):
	def __init__( self, env, renderer, py_int ):
		EeyValue.__init__( self, env, renderer )
		self.value = py_int

	def evaluate( self ):
		return self

	def plus( self, other ):
		# TODO: assert other is int
		return EeyInt( self.env, self.renderer, self.value + other.value )

class EeyString( EeyValue ):
	def __init__( self, env, renderer, py_str ):
		EeyValue.__init__( self, env, renderer )
		self.value = py_str

	def evaluate( self ):
		return self

class EeyPlus( EeyValue ):
	def __init__( self, env, renderer, left_value, right_value ):
		EeyValue.__init__( self, env, renderer )
		# TODO: assert( all( is_plusable, ( left_value, right_value ) )
		self.left_value  = left_value
		self.right_value = right_value

	def evaluate( self ):
		#if is_const( self.left_value ) and is_const( self.right_value ):
		#	return EeyInt( self.left_value + self.right_value )
		#else:
		#	return None
		return self.left_value.plus( self.right_value )

