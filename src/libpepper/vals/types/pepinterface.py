# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Truly I tell you, whatever you did for one of the least of these brothers and
# sisters of mine, you did for me.  Matt 25 v40

from libpepper.values import PepValue

class PepInterface( PepValue ):
    def __init__( self, name, base_interfaces, body_stmts ):
        PepValue.__init__( self )
        self.name = name
        self.base_interfaces = base_interfaces
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_interfaces, self.body_stmts )

#    def do_evaluate( self, env ):
#
#        nm = self.name.name()
#
#        if nm in env.namespace:
#            raise PepUserErrorException(
#                "The symbol '%s' is already defined." % nm )
#        else:
#            env.namespace[nm] = PepUserInterface(
#                nm, self.base_interfaces, self.body_stmts )
#
#        return self
    pass

