
from values import EeyValue
from functionvalues import EeyFunction

class EeyRuntimePrint( EeyValue ):
    def __init__( self, args ):
        self.args = args

class EeyPrint( EeyFunction ):

#    def __init__( self ):
#        EeyFunction.__init__( self, ( ( EeyAny, EeySymbol( "object" ) ), ) )

    def call( self, env, args ):
        return EeyRuntimePrint( args )


def add_builtins( env ):
    env.namespace["print"] = EeyPrint()
