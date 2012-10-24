from libeeyore.values import EeyValue

# TODO: test this class in isoloation

class EeyRange( EeyValue ):
    def __init__( self, begin, end, step ):
        EeyValue.__init__( self )
        self.begin = begin
        self.end   = end
        self.step  = step

    def construction_args( self ):
        return ( self.begin, self.end, self.step, )

    def do_evaluate( self, env ):
        return EeyRange(
            self.begin.evaluate( env ),
            self.end.evaluate( env ),
            self.step.evaluate( env )
        )

    @staticmethod
    def init( begin, end, step ):
        return EeyRange( begin, end, step )



