
from values import EeyArray
from values import EeyInt
from values import EeyValue

from usererrorexception import EeyUserErrorException

class EeyImport( EeyValue ):
	def __init__( self, module_name ):
		self.module_name = module_name

	def evaluate( self, env ):
		if self.module_name == "sys":
			import builtinmodules.eeysys
			builtinmodules.eeysys.add_names( env )
		else:
			raise EeyUserErrorException( "No module named %s" %
				self.module_name )
		return self

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
