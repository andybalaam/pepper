from itertools import izip

from namespace import EeyNamespace

class EeyEnvironment( object ):
	def __init__( self, renderer, namespace = None ):
		self.renderer = renderer
		if namespace is None:
			self.namespace = EeyNamespace()
		else:
			self.namespace = namespace

	def render_value( self, value ):
		return self.renderer.value_renderer( value )( self, value )

	def render_exe( self, values ):
		return self.renderer.render_exe( values, self )

	def clone_deeper( self, values, types_and_names ):
		"""Create a new environment based on this one, with
		the extra values provided stored in its namespace under
		the names provided."""

		ret = EeyEnvironment( self.renderer, EeyNamespace( self.namespace ) )

		for val, (UUtp, name) in izip( values, types_and_names ):
			ret.namespace[name.name()] = val

		print ret.namespace.thedict

		return ret


