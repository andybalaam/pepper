
class EeyNamespace( dict ):

#	def __getitem__( self, key ):
#		pass

	def __setitem__( self, key, value ):
		assert( key not in self ) # TODO - not an assert
		dict.__setitem__( self, key, value )


