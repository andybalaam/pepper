# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Truly I tell you, whatever you did for one of the least of these brothers and
# sisters of mine, you did for me.  Matt 25 v40

from libpepper.values import PepBool
from libpepper.values import PepType
from libpepper.values import PepValue

from pepuserinterface import PepUserInterface

class PepInterface( PepValue ):
    """
    The value created when an interface is parsed in source code.
    An interface allows specifying which types of object are acceptable as
    parameters to a particular function.
    At the moment, this is done only by saying "the following method signatures
    must be found within this type," but in future interfaces will be allowed
    to specify the existence of global methods, data members, and inheritance
    from other interfaces will be allowed.
    """

    def __init__( self, name, base_interfaces, body_stmts ):
        PepValue.__init__( self )
        self.name = name
        self.base_interfaces = base_interfaces
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_interfaces, self.body_stmts )

    def do_evaluate( self, env ):

        nm = self.name.name()

        if nm in env.namespace:
            raise PepUserErrorException(
                "The symbol '%s' is already defined." % nm )
        else:
            env.namespace[nm] = PepUserInterface(
                nm, self.base_interfaces, self.body_stmts )

        return self

    def ct_eval( self, env ):
        return self.evaluate( env )

