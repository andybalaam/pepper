# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from abc import ABCMeta, abstractmethod

from all_known import all_known
from pepinterface import implements_interface
from usererrorexception import PepUserErrorException
from utils.type_is import type_is

# -- Base class and global methods ---

class PepValue( object ):

    __metaclass__ = ABCMeta

    def __init__( self ):
        self.cached_eval = None
        self.cached_eval_env = None

    def render( self, env ):
        return env.render_value( self.evaluate( env ) )

    def is_known( self, env ):
        return True

    def evaluate( self, env ):
        if self.cached_eval is None or env is not self.cached_eval_env:
            self.cached_eval = self.do_evaluate( env )
            self.cached_eval_env = env

        return self.cached_eval

    def do_evaluate( self, env ):
        return self

    def evaluated_type( self, env ):
        return PepType( self.__class__ )

    @abstractmethod
    def construction_args( self ): pass

    def __repr__( self ):
        return "%s(%s)" % (
            self.__class__.__name__,
            ",".join( repr(x) for x in self.construction_args() )
            )

# --- Specific value types ---


class PepSymbol( PepValue ):
    def __init__( self, symbol_name ):
        PepValue.__init__( self )
        self.symbol_name = symbol_name

    def construction_args( self ):
        return ( self.symbol_name, )

    def __eq__( self, other ):
        return (
            self.__class__ == other.__class__ and
            self.symbol_name == other.symbol_name
        )

    def __ne__( self, other ):
        return not self.__eq__( other )

    def _check_contains( self, namespace, name, base_sym ):
        if name not in namespace:
            raise PepUserErrorException(
                ( "The symbol '%s' is not defined in '%s'." % (
                    name, base_sym ) )
            )
            # TODO: line, column, filename
            # TODO: say where we were looking


    def _do_find_namespace_and_name( self, sym, base_sym, namespace, env ):
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
            self._check_contains( namespace, this_ns_name, base_sym )

            if base_sym != "":
                base_sym += "."
            base_sym += this_ns_name

            new_ns_holder = namespace[this_ns_name].evaluate( env )

            if not hasattr( new_ns_holder.__class__, "get_namespace" ):
                raise PepUserErrorException(
                    (
                        "The value %s at '%s' is not a " +
                        "class, object or module, so you can't look up " +
                        "values in it as in the expression '%s'"
                    ) % ( new_ns_holder.__class__, this_ns_name, sym )
                )

            new_ns = new_ns_holder.get_namespace()

            return self._do_find_namespace_and_name(
                spl[1], base_sym, new_ns, env )

    def _lookup( self, env ):
        (namespace, name, base_sym) = self._do_find_namespace_and_name(
            self.symbol_name, "", env.namespace, env )

        self._check_contains( namespace, name, base_sym )
        return namespace[name]

    def find_namespace_and_name( self, env ):
        return self._do_find_namespace_and_name(
            self.symbol_name, "", env.namespace, env )

    def name( self ):
        # TODO: delete this method, or use it consistently
        return self.symbol_name

    def do_evaluate( self, env ):
        # Look up this symbol in the namespace of our environment
        value = self._lookup( env ).evaluate( env )

        if value.is_known( env ):
            # Pass back what we looked up
            return value
        elif implements_interface( value, PepSymbol ):
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

class PepBool( PepValue ):
    def __init__( self, value ):
        PepValue.__init__( self )
        self.value = value

    def construction_args( self ):
        return ( self.value, )


class PepNoneType( PepValue ):
    def construction_args( self ):
        return ()

pep_none = PepNoneType()


class PepVoid( PepValue ):
    def construction_args( self ):
        return ()


class PepString( PepValue ):
    def __init__( self, py_str ):
        PepValue.__init__( self )
        self.value = py_str

    def construction_args( self ):
        return ( self.value, )

    def as_py_str( self ):
        return self.value

class PepBinaryOp( PepValue ):
    def __init__( self, left_value, right_value ):
        PepValue.__init__( self )
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


class PepPlus( PepBinaryOp ):
    def operator( self, lv, rv ):
        return lv.plus( rv )

class PepTimes( PepBinaryOp ):
    def operator( self, lv, rv ):
        return lv.times( rv )

class PepGreaterThan( PepBinaryOp ):
    def operator( self, lv, rv ):
        return lv.greater_than( rv )

    def evaluated_type( self, env ):
        return PepType( PepBool )


class PepPass( PepValue ):
    """A statement that does nothing."""

    def __init__( self ):
        PepValue.__init__( self )

    def construction_args( self ):
        return ()

class PepTypeMatcher():
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
    def runtime_namespace( self, instance, insert_placeholders ):
        """
        @return a namespace representing the allowed properties and method
                names in an instance of this type
        """
        pass

    @abstractmethod
    def get_namespace( self ):
        """
        @return a namespace representing the allowed properties and method
                names in this type
        """
        pass


class PepEmptyNamespace( object ):

    def __contains__( self, key ):
        return False

    def __getitem__( self, key ):
        return None

    def __setitem__( self, key, value ):
        pass

    def key_for_value( self, value ):
        return None

class PepType( PepValue, PepTypeMatcher ):
    """
    A type which is directly representable as a Python class e.g. PepInt
    """

    def __init__( self, value ):
        PepValue.__init__( self )
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

    def runtime_namespace( self, instance, insert_placeholders ):
        #type_implements( PepValueWithNamespace, instance )
        type_is( bool, insert_placeholders )
        # For simple types, there are no methods or properties
        # yet, so we can return an empty namespace.
        # TODO: support methods on e.g. ints, meaning we need
        #       a PepInstanceNamespace, and can maybe combine
        #       this code with that in PepUserClass?
        return self.get_namespace()

    def get_namespace( self ):
        return PepEmptyNamespace()

    def __eq__( self, other ):
        return (
            self.__class__ == other.__class__ and
            self.value == other.value
        )

    def __ne__( self, other ):
        return not self.__eq__( other )

class PepArray( PepValue ):
    def __init__( self, value_type, values ):
        PepValue.__init__( self )
        self.value_type = value_type
        self.values = values

    def construction_args( self ):
        return ( self.value_type, self.values )

    def get_index( self, int_index ):
        return self.values[int_index]



