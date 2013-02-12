# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from libpepper.vals.all_values import *

from libpepper.usererrorexception import PepUserErrorException

class PepRuntimePrint( PepValue ):
    def __init__( self, args ):
        PepValue.__init__( self )
        self.args = args

    def construction_args( self ):
        return ( self.args, )

class PepPrint( PepFunction ):

#    def __init__( self ):
#        PepFunction.__init__( self, ( ( PepAny, PepSymbol( "object" ) ), ) )

    def construction_args( self ):
        return ()

    def call( self, args, env ):
        return PepRuntimePrint( args )

    def return_type( self, args, env ):
        return PepType( PepNoneType )

    def args_match( self, args, env ):
        return True # Print accepts anything


class PepRuntimeLen( PepValue ):
    def __init__( self, args ):
        PepValue.__init__( self )
        if( len( args ) != 1 ):
            raise UserErrorException(
                "There should only ever be one argument to len()" )
        self.arg = args[0]

    def construction_args( self ):
        return ( (self.arg,), )

    def do_evaluate( self, env ):
        # TODO: if it's known, do it
        return self

    def is_known( self, env ):
        # TODO: if it's known, return True
        return False

class PepLen( PepFunction ):
    def construction_args( self ):
        return ()

    def call( self, args, env ):
        return PepRuntimeLen( args )

    def return_type( self, args, env ):
        return PepType( PepInt )

    def args_match( self, args, env ):
        return True # TODO

# TODO: write this in pepper
range_function = PepUserFunction(
    "range_impl",
    PepType( PepRange ),
    (
        ( PepType( PepInt ), PepSymbol( "begin" ) ),
        ( PepType( PepInt ), PepSymbol( "end" ) ),
        ( PepType( PepInt ), PepSymbol( "step" ), PepInt( "1" ) ),
    ),
    (
        # TODO: if end < begin and step was not supplied, default to -1
        PepReturn( PepRange(
            PepSymbol( "begin" ), PepSymbol( "end" ), PepSymbol( "step" )
        ) ),
    )
)

class PepImplements( PepFunction ):

    def construction_args( self ):
        return ( arg, )

    def call( self, args, env ):
        if( len( args ) != 1 ):
            raise UserErrorException(
                "There should only ever be one argument to implements()" )
        return PepInterfaceTypeMatcher( args[0].evaluate( env ) )


    def return_type( self, args, env ):
        return PepType( PepBool )

    def args_match( self, args, env ):
        return True # TODO - only interfaces and classes accepted


def add_builtins( env ):
    # Statements
    env.namespace["pass"] = PepPass()

    # Values
    env.namespace["False"] = PepBool( False )
    env.namespace["True"]  = PepBool( True )

    # Types
    env.namespace["bool"]  = PepType( PepBool )
    env.namespace["float"] = PepType( PepFloat )
    env.namespace["int"]   = PepType( PepInt )
    env.namespace["string"]= PepType( PepString )
    env.namespace["void"]  = PepType( PepVoid )
    env.namespace["type"]  = PepType( PepType )
    env.namespace["code"]  = PepType( PepQuote )

    # Functions
    env.namespace["implements"] = PepImplements()
    env.namespace["len"]        = PepLen()
    env.namespace["print"]      = PepPrint()
    env.namespace["range"]      = range_function.evaluate( env )

