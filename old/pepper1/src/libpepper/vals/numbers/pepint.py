# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepBool
from libpepper.values import PepValue

class PepInt( PepValue ):
    def __init__( self,  str_int ):
        PepValue.__init__( self )
        self.value = str( str_int )

    def construction_args( self ):
        return ( self.value, )

    def plusequals( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        self.value = str( int( self.value ) + int( other.value ) )

    def plus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return PepInt( str( int( self.value ) + int( other.value ) ) )

    def minus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return PepInt( str( int( self.value ) - int( other.value ) ) )

    def times( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return PepInt( str( int( self.value ) * int( other.value ) ) )

    def greater_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return PepBool( int( self.value ) > int( other.value ) )

    def less_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return PepBool( int( self.value ) < int( other.value ) )


