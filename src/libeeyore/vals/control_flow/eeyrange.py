from libeeyore.values import EeyValue

# TODO: test this class in isoloation

class EeyRange( EeyValue ):
    def __init__( self, begin, end ):
        EeyValue.__init__( self )
        self.begin = begin
        self.end   = end

    def construction_args( self ):
        return ( self.begin, self.end, )

    def do_evaluate( self, env ):
        self.begin = self.begin.evaluate( env )
        self.end   = self.end.evaluate( env )
        return self

    @staticmethod
    def init( begin, end ):
        return EeyRange( begin, end )



