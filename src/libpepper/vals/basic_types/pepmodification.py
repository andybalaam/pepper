# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepValue
from libpepper.values import all_known

class PepModification( PepValue ):
    def __init__( self, var, mod_value ):
        PepValue.__init__( self )
        self.var = var
        self.mod_value = mod_value

    def construction_args( self ):
        return ( self.var, self.mod_value, )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            namespace, name, base_name = self.var.find_namespace_and_name( env )
            namespace[name].plusequals( self.mod_value.evaluate( env ) )
        return self

    def is_known( self, env ):
        return all_known( ( self.var, self.mod_value, ), env )



