from libeeyore.values import EeyBool
from libeeyore.values import EeyValue

class EeyInt( EeyValue ):
    def __init__( self,  str_int ):
        EeyValue.__init__( self )
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
        return EeyInt( str( int( self.value ) + int( other.value ) ) )

    def minus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyInt( str( int( self.value ) - int( other.value ) ) )

    def times( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyInt( str( int( self.value ) * int( other.value ) ) )

    def greater_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyBool( int( self.value ) > int( other.value ) )


