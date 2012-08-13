from values import EeyValue

class EeyQuote( EeyValue ):
    def __init__( self, code ):
        self.code = code

    def construction_args( self ):
        return ( self.code, )

