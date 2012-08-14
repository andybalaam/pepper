from values import EeyValue

class EeyQuote( EeyValue ):
    def __init__( self, statements ):
        EeyValue.__init__( self )
        self.statements = statements

    def construction_args( self ):
        return ( self.statements, )

    def execute( self ):
        return self.statements[-1]

