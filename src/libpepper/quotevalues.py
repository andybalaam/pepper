# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.namespace import EeyNamespace
from functionvalues import EeyFunction
from values import EeyValue


class EeyQuoteEvaluate( EeyFunction ):
    def __init__( self, quote ):
        EeyFunction.__init__( self )
        self.quote = quote

    def construction_args( self ):
        return ( self.quote, )

    def args_match( self, args ):
        return len( args ) == 0

    def call( self, args, env ):
        return self.quote.unquote().evaluate( env )

    def return_type( self, args, env ):
        return EeyType( EeyQuote )


class EeyQuote( EeyValue ):
    def __init__( self, statements ):
        EeyValue.__init__( self )
        self.statements = statements

    def construction_args( self ):
        return ( self.statements, )

    def unquote( self ):
        # TODO: Make a new value type which is a block of statements:
        #       probably shared with EeyUserFunction and other places?
        #       For now, just return the last statement.
        return self.statements[-1]

    def get_namespace( self ):
        ret = EeyNamespace()
        ret["evaluate"] = EeyQuoteEvaluate( self )
        return ret


