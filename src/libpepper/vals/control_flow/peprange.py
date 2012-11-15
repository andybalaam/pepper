# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.all_known import all_known
from libpepper.vals.numbers import PepInt
from libpepper.values import PepValue


class Iter( object ):
    def __init__( self, peprange ):
        # TODO: handle large numbers
        self.index = int( peprange.begin.value )
        self.end   = int( peprange.end.value )
        self.step  = int( peprange.step.value )

    def __iter__( self ):
        return self

    def next( self ):
        # TODO: handle large numbers
        if self.index >= self.end:
            raise StopIteration()
        ret = PepInt( str( self.index ) )
        self.index += self.step
        return ret


class PepRange( PepValue ):
    def __init__( self, begin, end, step ):
        PepValue.__init__( self )
        self.begin = begin
        self.end   = end
        self.step  = step

    def construction_args( self ):
        return ( self.begin, self.end, self.step, )

    def do_evaluate( self, env ):
        return PepRange(
            self.begin.evaluate( env ),
            self.end.evaluate( env ),
            self.step.evaluate( env )
        )

    def is_known( self, env ):
        return all_known( ( self.begin, self.end, self.step ), env )

    @staticmethod
    def init( begin, end, step ):
        return PepRange( begin, end, step )

    def __iter__( self ):
        return Iter( self )


