from abc import ABCMeta
from abc import abstractmethod

class EeyValue( object ):
	def __init__( self, env ):
		self.env = env

	def render( self ):
		return self.env.render_value( self.evaluate() )

class EeySymbol( EeyValue ):
	def __init__( self, env, symbol_name ):
		EeyValue.__init__( self, env )
		self.symbol_name = symbol_name

	def evaluate( self ):
		assert( self.symbol_name in self.env.namespace ) # TODO: not an assert
		return self.env.namespace[self.symbol_name]


class EeyInt( EeyValue ):
	def __init__( self, env, py_int ):
		EeyValue.__init__( self, env )
		self.value = py_int

	def evaluate( self ):
		return self

	def plus( self, other ):
		# TODO: assert other is int
		return EeyInt( self.env, self.value + other.value )

class EeyString( EeyValue ):
	def __init__( self, env, py_str ):
		EeyValue.__init__( self, env )
		self.value = py_str

	def evaluate( self ):
		return self

class EeyPlus( EeyValue ):
	def __init__( self, env, left_value, right_value ):
		EeyValue.__init__( self, env )
		# TODO: assert( all( is_plusable, ( left_value, right_value ) )
		self.left_value  = left_value
		self.right_value = right_value

	def evaluate( self ):
		#if is_const( self.left_value ) and is_const( self.right_value ):
		#	return EeyInt( self.left_value + self.right_value )
		#else:
		#	return None
		return self.left_value.plus( self.right_value )

