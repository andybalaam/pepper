
import cppvalues

class EeyCppRenderer( object ):
	def __init__( self ):
		self.headers = []

	def value_renderer( self, value ):
		return cppvalues.type2renderer[ value.__class__ ]
