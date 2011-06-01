
# -- Base class and global methods ---

class EeyValue( object ):

	def render( self, env ):
		return env.render_value( self.evaluate( env ) )

	def is_known( self, env ):
		return True

	def evaluate( self, env ):
		return self

def all_known( values, env ):
	return all( map( lambda v: v.is_known( env ), values ) )

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
		assert( self.symbol_name in env.namespace ) # TODO: not an assert
		return env.namespace[self.symbol_name]

	def evaluate( self, env ):
		# Look up this symbol in the namespace of our environment
		value = self._lookup( env ).evaluate( env )

		if value.is_known( env ):
			# Pass back what we looked up
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
			return self.left_value.plus( self.right_value )
		else:
			return self

	def is_known( self, env ):
		return all_known( ( self.left_value, self.right_value ), env )

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
			return fn.call( self.args )
		else:
			return self

