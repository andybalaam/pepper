# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.namespace import PepNamespace
from libpepper.vals.functions.pepfunction import PepFunction
from values import PepType
from values import PepValue


class PepQuoteEvaluate( PepFunction ):
    def __init__( self, quote ):
        PepFunction.__init__( self )
        self.quote = quote

    def construction_args( self ):
        return ( self.quote, )

    def args_match( self, args, env ):
        return len( args ) == 0

    def call( self, args, env ):
        return self.quote.unquote()

    def return_type( self, args, env ):
        return self.quote.unquote().evaluated_type( env )


class PepQuote( PepValue ):
    def __init__( self, statements ):
        PepValue.__init__( self )
        self.statements = statements

    def construction_args( self ):
        return ( self.statements, )

    def unquote( self ):
        # TODO: Make a new value type which is a block of statements:
        #       probably shared with PepUserFunction and other places?
        #       For now, just return the last statement.
        return self.statements[-1]

    def get_namespace( self ):
        ret = PepNamespace()
        ret["evaluate"] = PepQuoteEvaluate( self )
        return ret


