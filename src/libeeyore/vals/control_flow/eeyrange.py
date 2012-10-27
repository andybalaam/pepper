from libeeyore.all_known import all_known
from libeeyore.values import EeyInt
from libeeyore.values import EeyValue


class Iter( object ):
    def __init__( self, eeyrange ):
        # TODO: handle large numbers
        self.index = int( eeyrange.begin.value )
        self.end   = int( eeyrange.end.value )
        self.step  = int( eeyrange.step.value )

    def __iter__( self ):
        return self

    def next( self ):
        # TODO: handle large numbers
        if self.index >= self.end:
            raise StopIteration()
        ret = EeyInt( str( self.index ) )
        self.index += self.step
        return ret


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

    def is_known( self, env ):
        return all_known( ( self.begin, self.end, self.step ), env )

    @staticmethod
    def init( begin, end, step ):
        return EeyRange( begin, end, step )

    def __iter__( self ):
        return Iter( self )


