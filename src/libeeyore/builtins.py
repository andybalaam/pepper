
from values import EeyBool
from values import EeyValue
from functionvalues import EeyFunction

class EeyRuntimePrint( EeyValue ):
    def __init__( self, args ):
        self.args = args

    def construction_args( self ):
        return ( self.args, )

class EeyPrint( EeyFunction ):

#    def __init__( self ):
#        EeyFunction.__init__( self, ( ( EeyAny, EeySymbol( "object" ) ), ) )

    def construction_args( self ):
        return ()

    def call( self, env, args ):
        return EeyRuntimePrint( args )

class EeyRuntimeLen( EeyValue ):
    def __init__( self, args ):
        if( len( args ) != 1 ):
            raise UserErrorException(
                "There should only ever be one argument to len()" )
        self.arg = args[0]

    def construction_args( self ):
        return ( (arg,), )

    def evaluate( self, env ):
        # TODO: if it's known, do it
        return self

    def is_known( self ):
        # TODO: if it's known, return True
        return False

class EeyLen( EeyFunction ):
    def construction_args( self ):
        return ()

    def call( self, env, args ):
        return EeyRuntimeLen( args )


def add_builtins( env ):
    env.namespace["print"] = EeyPrint()
    env.namespace["len"] = EeyLen()
    env.namespace["True"] = EeyBool( True )
    env.namespace["False"] = EeyBool( False )
