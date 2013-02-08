# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from itertools import ifilter

from libpepper.environment import PepEnvironment
from libpepper.namespace import PepNamespace
from languagevalues import PepPlaceholder
from values import PepType
from values import PepTypeMatcher
from values import PepSymbol
from values import PepString
from values import PepValue
from values import PepVariable
from values import PepVoid
from values import all_known
from functionvalues import PepCallable
from functionvalues import PepDef
from functionvalues import PepFunction
from functionvalues import PepFunctionOverloadList
from functionvalues import PepRuntimeUserFunction
from usererrorexception import PepUserErrorException
from vals.types import PepDefInit
from vals.types import PepInitMethod
from vals.types import PepInstanceMethod
from vals.types import PepInstanceNamespace
from vals.types import PepKnownInstance
from vals.types import PepRuntimeInit
from vals.types import PepRuntimeInstance

INIT_METHOD_NAME = "init"



class PepUserClass( PepValue, PepTypeMatcher ):
    def __init__( self, name, base_classes, body_stmts ):
        PepValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert
        self.namespace = None

    def is_known( self, env ):
        return True # TODO - not always known

    def runtime_instance( self, name ):
        return PepRuntimeInstance( self, name )

    def known_instance( self ):
        return PepKnownInstance( self )

    def do_evaluate( self, env ):
        self.namespace = PepNamespace( env.namespace )
        subenv = PepEnvironment( env.renderer, self.namespace )
        for st in self.body_stmts:
            st.evaluate( subenv )

        if INIT_METHOD_NAME in self.namespace:
            raise PepUserErrorException( "You may not define the symbol " +
                "'%s' in a class definition." % INIT_METHOD_NAME )

        # TODO: disallow defining functions called __init__

        self.namespace[INIT_METHOD_NAME] = PepInitMethod( self )

        self.member_variables = self._find_member_variables()

        for var_type, var_name in self.member_variables:
            self.namespace[var_name] = PepPlaceholder()

        return self

    def _find_member_variables( self ):
        ret = []

        first_def_init = True
        is_def_init = lambda stmt: stmt.__class__ == PepDefInit
        for stmt in ifilter( is_def_init, self.body_stmts ):
            if first_def_init:
                ret = stmt.get_member_variables()
            else:
                self.check_init_matches( ret )
            first_def_init = False

        return ret

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def matches( self, other ):
        """
        @return True if other is this class.
        """
        return ( other == self )

    def get_name( self ):
        return self.name

    def underlying_class( self ):
        return self

    def get_namespace( self ):
        return self.namespace


class PepClass( PepValue ):
    def __init__( self, name, base_classes, body_stmts ):
        PepValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def do_evaluate( self, env ):

        nm = self.name.name()

        if nm in env.namespace:
            raise PepUserErrorException(
                "The symbol '%s' is already defined." % nm )
             # TODO: line, column, filename
        else:
            env.namespace[nm] = PepUserClass(
                nm, self.base_classes, self.body_stmts )

        return self

    def check_init_matches( self, var_names ):
        pass # TODO: ensure later def_inits match the first one

