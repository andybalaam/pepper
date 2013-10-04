# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# So God created the great creatures of the sea and every living thing with
# which the water teems and that moves about in it, according to their kinds,
# and every winged bird according to its kind. And God saw that it was good.
# Genesis 1 v21

from libpepper.environment import PepEnvironment
from libpepper.functionvalues import PepFunctionOverloadList
from libpepper.namespace import PepNamespace
from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

from pepdefinit import PepDefInit
from pepimplementsfunction import PepImplementsFunction
from pepinitfunction import PepInitFunction
from pepinterfacematchesfunction import PepInterfaceMatchesFunction
from pepknowninstance import PepKnownInstance

from libpepper.usererrorexception import PepUserErrorException

MATCHES_FUNCTION_NAME = "matches"

class PepUserInterface( PepValue ):
    """
    A user-defined interface, created when we evaluate a PepInterface.
    Provides a matches function that returns true if the supplied type
    matches this interface.
    """

    def __init__( self, name, base_interfaces, body_stmts, namespace = None ):
        PepValue.__init__( self )
        self.name = name
        self.base_interfaces = base_interfaces
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert
        self.namespace = namespace

    def is_known( self, env ):
        return True # TODO - not always known

    def check_symbol_not_defined( self, symbol ):
        if symbol in self.namespace:
            raise PepUserErrorException( "You may not define the symbol " +
                "'%s' in an interface definition." % symbol )

    def do_evaluate( self, env ):
        # TODO: share code with PepUserClass
        self.namespace = PepNamespace( env.namespace )
        subenv = PepEnvironment( env.renderer, self.namespace )
        for st in self.body_stmts:
            st.evaluate( subenv )

        self.check_symbol_not_defined( MATCHES_FUNCTION_NAME )

        self.namespace[MATCHES_FUNCTION_NAME] = PepFunctionOverloadList(
            ( PepInterfaceMatchesFunction( self ), )
        )

        return self

    def evaluated_type( self, env ):
        return self

    def construction_args( self ):
        return ( self.name, self.base_interfaces, self.body_stmts )

    def can_match( self, other, env ):
        """
        Decide whether the type other matches this interface.

        Deliberately not called "matches" since an instance of this class
        is not a TypeMatcher, but must be wrapped with a call to the
        "implements" function.

        @return True if other has all the methods we define.
        """

        otherns = other.get_namespace()
        for stmt in self.body_stmts:
            if stmt.name.name() not in otherns:
                #print "Nothing with this name", stmt.name.name()
                return False # Nothing with this name
            othermeth = otherns[stmt.name.name()]
            if othermeth.__class__ != PepFunctionOverloadList:
                #print "Thing with this name is not a method", stmt.name.name()
                return False # Thing with this name is not a method
            if not othermeth.signature_matches(
                stmt.ret_type, stmt.arg_types_and_names, env
            ):
                #print "No matching signature", stmt.ret_type, stmt.arg_types_and_names
                return False # No matching signature
        return True

    def get_name( self ):
        return self.name

    def underlying_class( self ):
        return self

    def get_namespace( self ):
        return self.namespace

