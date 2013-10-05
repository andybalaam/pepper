# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# In his great power God becomes like clothing to me; he binds me like the neck
# of my garment.  Job 30 v18

from libpepper.values import all_known

from libpepper.vals.functions.pepfunction import PepFunction
from libpepper.vals.functions.pepruntimeuserfunction import PepRuntimeUserFunction

class PepInstanceMethod( PepFunction ):
    """
    A method that is bound to an instance of a class.  Acts like a function
    that can be called independently, because it carries its own "self"
    around with it.
    """

    def __init__( self, instance, fn ):
        # TODO: type_is_one_of( (PepVariable, PepKnownInstance), instance )

        PepFunction.__init__( self )
        self.instance = instance
        self.fn = fn

    def construction_args( self ):
        return ( self.instance, self.fn )

    def _instance_plus_args( self, args ):
        return (self.instance,) + args

    def call( self, args, env ):
        if all_known( args + (self.instance,), env ):
            return self.fn.call( self._instance_plus_args( args ), env )
        else:
            return PepRuntimeUserFunction(
                self.fn,
                self._instance_plus_args( args ),
                self.instance.clazz.get_name()
            )

    def return_type( self, args, env ):
        return self.fn.return_type( self._instance_plus_args( args ), env )

    def args_match( self, args, env ):
        return self.fn.args_match( self._instance_plus_args( args ), env )

    def is_known( self, env ):
        return self.instance.is_known( env )

