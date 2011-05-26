
from namespace import EeyNamespace

class EeyEnvironment( object ):
	def __init__( self, renderer ):
		self.renderer = renderer
		self.namespace = EeyNamespace()

	def render_value( self, value ):
		return self.renderer.value_renderer( value )( self, value )

