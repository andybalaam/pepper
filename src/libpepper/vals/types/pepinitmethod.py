# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Start children off on the way they should go, and even when they are old they
# will not turn from it.  Proverbs 22 v6

from libpepper.functionvalues import PepFunction
from libpepper.values import all_known

from pepdefinit import PepDefInit
from pepknowninstance import PepKnownInstance
from pepruntimeinit import PepRuntimeInit

class PepInitMethod( PepFunction ):
    """
    A function automatically present in every user-defined class called "init"
    that returns a new instance of this class.  It uses the relevant def_init
    method of the class as part of the construction process.
    """

    def __init__( self, user_class ):
        PepFunction.__init__( self )
        self.user_class = user_class

    def call( self, args, env ):
        if all_known( args, env ):
            ret = self.user_class.known_instance()
            if PepDefInit.INIT_IMPL_NAME in self.user_class.namespace:
                self.user_class.namespace[PepDefInit.INIT_IMPL_NAME].call(
                    (ret,) + args, env )
            # TODO: else default constructor
            return ret
        else:
            inst = self.user_class.runtime_instance( "" )
            return PepRuntimeInit(
                inst,
                args,
                self.user_class.namespace[PepDefInit.INIT_IMPL_NAME].call(
                    (inst,) + args, env )
            )

    def return_type( self, args, env ):
        return self.user_class

    def args_match( self, args ):
        if PepDefInit.INIT_IMPL_NAME not in self.user_class.namespace:
            # If there is no __init__, we will supply an empty constructor
            return ( len( args ) == 0 )

        # Make an object that looks like an instance so it passes the
        # call to matches() on the PepUserClass, and put it on the beginning
        # of the args array before we match against the user-defined init
        # method.
        self_plus_args = [ PepKnownInstance( self.user_class ) ] + args

        return self.user_class.namespace[PepDefInit.INIT_IMPL_NAME].args_match(
            self_plus_args )

    def construction_args( self ):
        return ( self.user_class, )

