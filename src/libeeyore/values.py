
# -- Base class and global methods ---

class EeyValue( object ):

	def __init__( self, env ):
		self.env = env

	def render( self ):
		return self.env.render_value( self.evaluate() )

	def is_const( self ):
		return True

def all_const( values ):
	return all( map( lambda v: v.is_const(), values ) )

# --- Specific value types ---

class EeyVariable( EeyValue ):
	def __init__( self, env, clazz ):
		EeyValue.__init__( self, env )
		self.clazz = clazz

	def evaluate( self ):
		return self

	def is_const( self ):
		return False

class EeySymbol( EeyValue ):
	def __init__( self, env, symbol_name ):
		EeyValue.__init__( self, env )
		self.symbol_name = symbol_name

	def _lookup( self ):
		assert( self.symbol_name in self.env.namespace ) # TODO: not an assert
		return self.env.namespace[self.symbol_name]

	def evaluate( self ):
		# Look up this symbol in the namespace of our environment
		value = self._lookup().evaluate()

		if value.is_const():
			# Pass back what we looked up
			return value
		else:
			# If what we find is a variable (i.e. something unknown until
			# runtime) then we simply return ourselves: for the purpose of
			# rendering, this _is_ a symbol.
			return self

	def is_const( self ):
		return self._lookup().is_const()


class EeyInt( EeyValue ):
	def __init__( self, env, py_int ):
		EeyValue.__init__( self, env )
		self.value = py_int

	def evaluate( self ):
		return self

	def plus( self, other ):
		assert other.__class__ == self.__class__
		return EeyInt( self.env, self.value + other.value )

class EeyString( EeyValue ):
	def __init__( self, env, py_str ):
		EeyValue.__init__( self, env )
		self.value = py_str

	def evaluate( self ):
		return self

	def as_py_str( self ):
		return self.value

class EeyPlus( EeyValue ):
	def __init__( self, env, left_value, right_value ):
		EeyValue.__init__( self, env )
		# TODO: assert( all( is_plusable, ( left_value, right_value ) )
		self.left_value  = left_value
		self.right_value = right_value

	def evaluate( self ):
		if self.is_const():
			return self.left_value.plus( self.right_value )
		else:
			return self

	def is_const( self ):
		return all_const( ( self.left_value, self.right_value ) )

def is_callable( value ):
	return True # TODO: check whether the object may be called

class EeyFunctionCall( EeyValue ):
	def __init__( self, env, func, args ):
		EeyValue.__init__( self, env )
		self.func = func
		self.args = args

	def evaluate( self ):
		if all_const( self.args ):
			fn = self.func.evaluate()
			assert is_callable( fn )
			return fn.call( self.args )
		else:
			return self

