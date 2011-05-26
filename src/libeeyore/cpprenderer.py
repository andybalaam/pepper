
import cppvalues
		
class EeyCppRenderer( object ):
	def value_renderer( self, value ):
		return cppvalues.type2renderer[ value.__class__ ]
