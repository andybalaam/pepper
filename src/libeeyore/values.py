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
        return EeyType( self.__class__ )

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
        return self.clazz.evaluate( env )

    def get_namespace( self ):
        return self.clazz.get_namespace()


class EeySymbol( EeyValue ):
    def __init__( self, symbol_name ):
        EeyValue.__init__( self )
        self.symbol_name = symbol_name

    def construction_args( self ):
        return ( self.symbol_name, )

    def _check_contains( self, namespace, name, base_sym ):
        if name not in namespace:
            raise EeyUserErrorException(
                ( "The symbol '%s' is not defined in '%s'." % (
                    name, base_sym ) )
            )
            # TODO: line, column, filename
            # TODO: say where we were looking


    def _do_find_namespace_and_name( self, sym, base_sym, env, namespace ):
        """
        @return (namespace, name, base_name) where:
                    namespace is the namespace in which this symbol is found
                    name      is the string name of it
                    base_sym  is the qualified name of the object in which
                              it is found
        """

        spl = sym.split( '.', 1 )

        this_ns_name = spl[0]

        if len( spl ) == 1: # No more dotted elements in the name, return
            return ( namespace, this_ns_name, base_sym )
        else:
            if base_sym != "":
                base_sym += "."
            base_sym += this_ns_name
            self._check_contains( namespace, this_ns_name, base_sym )

            new_ns_holder = namespace[this_ns_name].evaluate( env )

            if not hasattr( new_ns_holder.__class__, "get_namespace" ):
                raise EeyUserErrorException(
                    (
                        "The value %s at '%s' is not a " +
                        "class, object or module, so you can't look up " +
                        "values in it as in the expression '%s'"
                    ) % ( new_ns_holder.__class__, this_ns_name, sym )
                )

            new_ns = new_ns_holder.get_namespace()

            return self._do_find_namespace_and_name(
                spl[1], base_sym, env, new_ns )

    def _lookup( self, env ):
        (namespace, name, base_sym) = self._do_find_namespace_and_name(
            self.symbol_name, "", env, env.namespace )

        self._check_contains( namespace, name, base_sym )
        return namespace[name]

    def find_namespace_and_name( self, env ):
        return self._do_find_namespace_and_name(
            self.symbol_name, "", env, env.namespace )

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

class EeyBinaryOp( EeyValue ):
    def __init__( self, left_value, right_value ):
        EeyValue.__init__( self )
        # TODO: assert( all( self.is_applicable, ( left_value, right_value ) )
        self.left_value  = left_value
        self.right_value = right_value

    def construction_args( self ):
        return ( self.left_value, self.right_value )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            lv = self.left_value.evaluate( env )
            rv = self.right_value.evaluate( env )
            return self.operator( lv, rv )
        else:
            return self

    def evaluated_type( self, env ):
        return self.left_value.evaluated_type( env )

    def is_known( self, env ):
        return all_known( ( self.left_value, self.right_value ), env )


class EeyPlus( EeyBinaryOp ):
    def operator( self, lv, rv ):
        return lv.plus( rv )

class EeyTimes( EeyBinaryOp ):
    def operator( self, lv, rv ):
        return lv.times( rv )

class EeyGreaterThan( EeyBinaryOp ):
    def operator( self, lv, rv ):
        return lv.greater_than( rv )

    def evaluated_type( self, env ):
        return EeyType( EeyBool )


class EeyPass( EeyValue ):
    """A statement that does nothing."""

    def __init__( self ):
        EeyValue.__init__( self )

    def construction_args( self ):
        return ()

class EeyTypeMatcher():
    __metaclass__ = ABCMeta

    @abstractmethod
    def matches( self, value_type ):
        """
        @return True if the supplied value_type matches this matcher
        """
        pass

    @abstractmethod
    def get_name( self ):
        """
        @return a string representation of this type
        """
        pass

    @abstractmethod
    def underlying_class( self ): pass

    @abstractmethod
    def get_namespace( self ):
        """
        @return a namespace representing the allowed properties and method
                names in this type
        """
        pass


class EeyEmptyNamespace( object ):

    def __contains__( self, key ):
        return False

    def __getitem__( self, key ):
        return None

    def __setitem__( self, key, value ):
        pass

    def key_for_value( self, value ):
        return None

class EeyType( EeyValue, EeyTypeMatcher ):
    """
    A type which is directly representable as a Python class e.g. EeyInt
    """

    def __init__( self, value ):
        EeyValue.__init__( self )
        # TODO: check we have been passed a type
        self.value = value

    def matches( self, other ):
        return ( self == other )

    def get_name( self ):
        return self.value.__name__

    def construction_args( self ):
        return ( self.value, )

    def underlying_class( self ):
        return self.value

    def get_namespace( self ):
        return EeyEmptyNamespace()

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



