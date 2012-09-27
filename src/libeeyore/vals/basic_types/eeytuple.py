from libeeyore.values import EeyValue

class EeyTuple( EeyValue ):
    def __init__( self, items ):
        EeyValue.__init__( self )
        self.items = items

    def construction_args( self ):
        return ( self.items, )

