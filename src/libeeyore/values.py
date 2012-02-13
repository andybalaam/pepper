from abc import ABCMeta, abstractmethod

from all_known import all_known
from eeyinterface import implements_interface
from usererrorexception import EeyUserErrorException

# -- Base class and global methods ---

class EeyValue( object ):

    __metaclass__ = ABCMeta

    def __init__( self ):
        self.cached_eval = None

    def render( self, env ):
        return env.render_value( self.evaluate( env ) )

    def is_known( self, env ):
        return True

    def evaluate( self, env ):
        if self.cached_eval is None:
            self.cached_eval = self.do_evaluate( env )
        return self.cached_eval

    def do_evaluate( self, env ):
        return self

    def evaluated_type( self, env ):
        return self.__class__

    @abstractmethod
    def construction_args( self ): pass

    def __repr__( self ):
        return "%s(%s)" % (
            self.__class__.__name__,
            ",".join( repr(x) for x in self.construction_args() )
            )

# --- Specific value types ---

class EeyVariable( EeyValue ):
    def __init__( self, clazz ):
        EeyValue.__init__( self )
        self.clazz = clazz

    def construction_args( self ):
        return ( self.clazz, )

    def is_known( self, env ):
        return False

    def evaluated_type( self, env ):
        return self.clazz

class EeySymbol( EeyValue ):
    def __init__( self, symbol_name ):
        EeyValue.__init__( self )
        self.symbol_name = symbol_name

    def construction_args( self ):
        return ( self.symbol_name, )

    def _lookup( self, env ):
        if self.symbol_name not in env.namespace:
            raise EeyUserErrorException( "The symbol '%s' is not defined." %
                self.symbol_name )
            # TODO: line, column, filename

        return env.namespace[self.symbol_name]

    def name( self ):
        # TODO: delete this method, or use it consistently
        return self.symbol_name

    def do_evaluate( self, env ):
        # Look up this symbol in the namespace of our environment
        value = self._lookup( env ).evaluate( env )

        if value.is_known( env ):
            # Pass back what we looked up
            return value
        elif implements_interface( value, EeySymbol ):
            return value
        else:
            # If what we find is a variable (i.e. something unknown until
            # runtime) then we simply return ourselves: for the purpose of
            # rendering, this _is_ a symbol.
            return self

    def is_known( self, env ):
        return self._lookup( env ).is_known( env )

    def evaluated_type( self, env ):
        return self._lookup( env ).evaluated_type( env )

class EeyBool( EeyValue ):
    def __init__( self, value ):
        EeyValue.__init__( self )
        self.value = value

    def construction_args( self ):
        return ( self.value, )


class EeyInt( EeyValue ):
    def __init__( self,  str_int ):
        EeyValue.__init__( self )
        self.value = str( str_int )

    def construction_args( self ):
        return ( self.value, )

    def plus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyInt( str( int( self.value ) + int( other.value ) ) )

    def times( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyInt( str( int( self.value ) * int( other.value ) ) )

    def greater_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle large numbers
        return EeyBool( int( self.value ) > int( other.value ) )


class EeyFloat( EeyValue ):
    def __init__( self,  str_float ):
        EeyValue.__init__( self )
        self.value = str( str_float )

    def construction_args( self ):
        return ( self.value, )

    def plus( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return EeyFloat( str( float( self.value ) + float( other.value ) ) )

    def times( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return EeyFloat( str( float( self.value ) * float( other.value ) ) )

    def greater_than( self, other ):
        assert other.__class__ == self.__class__
        # TODO: handle arbitrary numbers
        return EeyBool( float( self.value ) > float( other.value ) )


class EeyNoneType( EeyValue ):
    def construction_args( self ):
        return ()

eey_none = EeyNoneType()


class EeyVoid( EeyValue ):
    def construction_args( self ):
        return ()


class EeyString( EeyValue ):
    def __init__( self, py_str ):
        EeyValue.__init__( self )
        self.value = py_str

    def construction_args( self ):
        return ( self.value, )

    def as_py_str( self ):
        return self.value

class EeyPlus( EeyValue ):
    def __init__( self, left_value, right_value ):
        EeyValue.__init__( self )
        # TODO: assert( all( is_plusable, ( left_value, right_value ) )
        self.left_value  = left_value
        self.right_value = right_value

    def construction_args( self ):
        return ( self.left_value, self.right_value )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            return self.left_value.evaluate( env ).plus(
                self.right_value.evaluate( env ) )
        else:
            return self

    def evaluated_type( self, env ):
        return self.left_value.evaluated_type( env )

    def is_known( self, env ):
        return all_known( ( self.left_value, self.right_value ), env )


class EeyTimes( EeyValue ):
    def __init__( self, left_value, right_value ):
        EeyValue.__init__( self )
        # TODO: assert( all( is_timesable, ( left_value, right_value ) )
        self.left_value  = left_value
        self.right_value = right_value

    def construction_args( self ):
        return ( self.left_value, self.right_value )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            return self.left_value.evaluate( env ).times(
                self.right_value.evaluate( env ) )
        else:
            return self

    def evaluated_type( self, env ):
        return self.left_value.evaluated_type( env )

    def is_known( self, env ):
        return all_known( ( self.left_value, self.right_value ), env )


class EeyGreaterThan( EeyValue ):
    def __init__( self, left_value, right_value ):
        EeyValue.__init__( self )
        # TODO: assert( all( is_gtable, ( left_value, right_value ) )
        self.left_value  = left_value
        self.right_value = right_value

    def construction_args( self ):
        return ( self.left_value, self.right_value )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            return self.left_value.evaluate( env ).greater_than(
                self.right_value.evaluate( env ) )
        else:
            return self

    def is_known( self, env ):
        return all_known( ( self.left_value, self.right_value ), env )


class EeyPass( EeyValue ):
    """A statement that does nothing."""

    def __init__( self ):
        EeyValue.__init__( self )

    def construction_args( self ):
        return ()

class EeyType( EeyValue ):
    def __init__( self, value ):
        EeyValue.__init__( self )
        # TODO: check we have been passed a type
        self.value = value

    def construction_args( self ):
        return ( self.value, )

    def __eq__( self, other ):
        return (
            self.__class__ == other.__class__ and
            self.value == other.value
        )

    def __ne__( self, other ):
        return not self.__eq__( other )

class EeyArray( EeyValue ):
    def __init__( self, value_type, values ):
        EeyValue.__init__( self )
        self.value_type = value_type
        self.values = values

    def construction_args( self ):
        return ( self.value_type, self.values )

    def get_index( self, int_index ):
        return self.values[int_index]



