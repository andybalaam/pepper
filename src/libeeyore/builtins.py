# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from libeeyore.vals.all_values import *

class EeyRuntimePrint( EeyValue ):
    def __init__( self, args ):
        EeyValue.__init__( self )
        self.args = args

    def construction_args( self ):
        return ( self.args, )

class EeyPrint( EeyFunction ):

#    def __init__( self ):
#        EeyFunction.__init__( self, ( ( EeyAny, EeySymbol( "object" ) ), ) )

    def construction_args( self ):
        return ()

    def call( self, args, env ):
        return EeyRuntimePrint( args )

    def return_type( self, args, env ):
        return EeyType( EeyNoneType )

    def args_match( self, args ):
        return True # Print accepts anything


class EeyRuntimeLen( EeyValue ):
    def __init__( self, args ):
        EeyValue.__init__( self )
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

class EeyLen( EeyFunction ):
    def construction_args( self ):
        return ()

    def call( self, args, env ):
        return EeyRuntimeLen( args )

    def return_type( self, args, env ):
        return EeyType( EeyInt )

    def args_match( self, args ):
        return True # TODO

# TODO: write this in eeyore
range_function = EeyUserFunction(
    "range_impl",
    EeyType( EeyRange ),
    (
        ( EeyType( EeyInt ), EeySymbol( "begin" ) ),
        ( EeyType( EeyInt ), EeySymbol( "end" ) ),
        ( EeyType( EeyInt ), EeySymbol( "step" ), EeyInt( "1" ) ),
    ),
    (
        # TODO: if end < begin and step was not supplied, default to -1
        EeyReturn( EeyRange(
            EeySymbol( "begin" ), EeySymbol( "end" ), EeySymbol( "step" )
        ) ),
    )
)

def add_builtins( env ):
    # Statements
    env.namespace["pass"] = EeyPass()

    # Values
    env.namespace["False"] = EeyBool( False )
    env.namespace["True"]  = EeyBool( True )

    # Types
    env.namespace["bool"]  = EeyType( EeyBool )
    env.namespace["float"] = EeyType( EeyFloat )
    env.namespace["int"]   = EeyType( EeyInt )
    env.namespace["string"]= EeyType( EeyString )
    env.namespace["void"]  = EeyType( EeyVoid )
    env.namespace["type"]  = EeyType( EeyType )
    env.namespace["code"]  = EeyType( EeyQuote )

    # Functions
    env.namespace["len"]   = EeyLen()
    env.namespace["print"] = EeyPrint()
    env.namespace["range"] = range_function.evaluate( env )

