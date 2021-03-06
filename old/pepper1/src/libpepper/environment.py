# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from itertools import izip

from namespace import PepNamespace

from values import PepType

class PepEnvironment( object ):
    def __init__( self, renderer, namespace = None ):
        self.renderer = renderer
        if namespace is None:
            self.namespace = PepNamespace()
        else:
            self.namespace = namespace

    def render_value( self, value ):
        return self.renderer.value_renderer( value )( value, self )

    def render_exe( self, values ):
        return self.renderer.render_exe( values, self )

    def clone_deeper( self ):
        """Create a new environment based on this one."""

        return PepEnvironment( self.renderer, PepNamespace( self.namespace ) )

    def pretty_name( self, value ):
        ret = self.namespace.key_for_value( value )

        # TODO: should never happen?
        if ret is None:
            return str( value )[:20]
        #assert ret is not None, (
        #    "Could not find " + str( value ) + " in namespace " +
        #    str( self.namespace.thedict )
        #)

        return ret


