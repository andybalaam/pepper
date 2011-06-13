
from all_known import all_known
from eeyinterface import implements_interface
from usererrorexception import EeyUserErrorException

# -- Base class and global methods ---

class EeyValue( object ):

	def render( self, env ):
		return env.render_value( self.evaluate( env ) )

	def is_known( self, env ):
		return True

	def evaluate( self, env ):
		return self

# --- Specific value types ---

class EeyVariable( EeyValue ):
	def __init__( self, clazz ):
		self.clazz = clazz

	def is_known( self, env ):
		return False

class EeySymbol( EeyValue ):
	def __init__( self, symbol_name ):
		self.symbol_name = symbol_name

	def _lookup( self, env ):
		if self.symbol_name not in env.namespace:
			raise EeyUserErrorException( "The symbol '%s' is not defined." %
				self.symbol_name )
			# TODO: line, column, filename

		return env.namespace[self.symbol_name]

	def name( self ):
		return self.symbol_name

	def evaluate( self, env ):
		# Look up this symbol in the namespace of our environment
		value = self._lookup( env ).evaluate( env )

		if value.is_known( env ):
			# Pass back what we looked up
			return value
		elif implements_interface( value, EeySymbol ):
			return value
		else:
			# If what we find is a variable (i.e. something unknown until
			# runtime) then we simply return ourselves: for the purpose of
			# rendering, this _is_ a symbol.
			return self

	def is_known( self, env ):
		return self._lookup( env ).is_known( env )


class EeyInt( EeyValue ):
	def __init__( self,  py_int ):
		self.value = py_int

	def plus( self, other ):
		assert other.__class__ == self.__class__
		return EeyInt( self.value + other.value )

class EeyString( EeyValue ):
	def __init__( self, py_str ):
		self.value = py_str

	def as_py_str( self ):
		return self.value

class EeyPlus( EeyValue ):
	def __init__( self, left_value, right_value ):
		# TODO: assert( all( is_plusable, ( left_value, right_value ) )
		self.left_value  = left_value
		self.right_value = right_value

	def evaluate( self, env ):
		if self.is_known( env ):
			return self.left_value.evaluate( env ).plus(
				self.right_value.evaluate( env ) )
		else:
			return self

	def is_known( self, env ):
		return all_known( ( self.left_value, self.right_value ), env )

class EeyDefine( EeyValue ):
	def __init__( self, symbol, value ):
		self.symbol = symbol
		self.value = value

	def evaluate( self, env ):
		name = self.symbol.name()

		if name in env.namespace:
			raise EeyUserErrorException( "The symbol '%s' is already defined." %
				name )
			# TODO: line, column, filename

		env.namespace[name] = self.value
		return self


class EeyPass( EeyValue ):
	"""A statement that does nothing."""
	pass # Perhaps unsurprisingly?

class EeyType( EeyValue ):
	def __init__( self, value ):
		# TODO: check we have been passed a type
		self.value = value


class EeyArray( EeyValue ):
	def __init__( self, value_type, values ):
		self.value_type = value_type
		self.values = values

	def get_index( self, int_index ):
		return self.values[int_index]



