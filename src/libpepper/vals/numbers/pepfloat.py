# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepBool
from libpepper.values import PepValue

class PepFloat( PepValue ):
    def __init__( self,  str_float ):
        PepValue.__init__( self )
        self.value = str( str_float )

    def construction_args( self ):
        return ( self.value, )

    def plusequals( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        self.value = str( float( self.value ) + float( other.value ) )

    def plus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return PepFloat( str( float( self.value ) + float( other.value ) ) )

    def times( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return PepFloat( str( float( self.value ) * float( other.value ) ) )

    def greater_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return PepBool( float( self.value ) > float( other.value ) )


