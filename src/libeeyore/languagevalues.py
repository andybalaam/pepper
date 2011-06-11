
from values import EeyArray
from values import EeyInt
from values import EeyValue

class EeyArrayLookup( EeyValue ):
	def __init__( self, array_value, index ):
		self.array_value = array_value
		self.index = index

	def evaluate( self, env ):
		idx = self.index.evaluate( env )
		arr = self.array_value.evaluate( env )
		assert( idx.__class__ == EeyInt )
		assert( arr.__class__ == EeyArray )
		return arr.values[idx.value].evaluate( env )
