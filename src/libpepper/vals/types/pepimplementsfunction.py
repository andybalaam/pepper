
from libpepper.functionvalues import PepFunction
from libpepper.values import PepBool
from libpepper.values import all_known

class PepImplementsFunction( PepFunction ):
    """
    A function automatically present in every class called "implements"
    that returns true if this class implements the supplied interface.
    """

    def __init__( self, clazz ):
        PepFunction.__init__( self )
        self.clazz = clazz

    def call( self, args, env ):
        if all_known( ( self.clazz,) + args, env ):
            evaldarg = args[0].evaluate( env )
            # TODO: check evaldarg is an interface (or at least has can_match)
            return PepBool( evaldarg.can_match( self.clazz ) )
        else:
            raise Exception(
                "Can't (currently) support checking whether classes " +
                "implement interfaces at runtime."
            )

    def return_type( self, args, env ):
        return self.clazz

    def args_match( self, args, env ):
        if PepDefInit.INIT_IMPL_NAME not in self.user_class.namespace:
            # If there is no __init__, we will supply an empty constructor
            return ( len( args ) == 0 )

        # Make an object that looks like an instance so it passes the
        # call to matches() on the PepUserClass, and put it on the beginning
        # of the args array before we match against the user-defined init
        # method.
        self_plus_args = [ PepKnownInstance( self.user_class ) ] + args

        return self.user_class.namespace[PepDefInit.INIT_IMPL_NAME].args_match(
            self_plus_args, env )

    def construction_args( self ):
        return ( self.clazz, )

