
from namespace import EeyNamespace

import builtins

class EeyEnvironment( object ):
	def __init__( self, renderer ):
		self.renderer = renderer
		self.namespace = EeyNamespace()
		builtins.add_builtins( self )

	def render_value( self, value ):
		return self.renderer.value_renderer( value )( self, value )

	def render_exe( self, values ):
		return self.renderer.render_exe( values, self )

