# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# It is I who made the earth and created mankind on it. My own hands stretched
# out the heavens; I marshalled their starry hosts.  Isaiah 45 v12

from itertools import ifilter

from libpepper.environment import PepEnvironment
from libpepper.languagevalues import PepPlaceholder
from libpepper.namespace import PepNamespace
from libpepper.values import PepTypeMatcher
from libpepper.values import PepValue

from pepdefinit import PepDefInit
from pepinitmethod import PepInitMethod
from pepknowninstance import PepKnownInstance
from pepruntimeinstance import PepRuntimeInstance

from libpepper.usererrorexception import PepUserErrorException

INIT_METHOD_NAME = "init"

class PepUserClass( PepValue, PepTypeMatcher ):
    """
    A user-defined class, created when we evaluate a PepClass.  The class
    itself contains an ordinary namespace, and instances of this class
    piggy-back on that namespace to provide their own special
    PepInstanceNamespace that binds methods to instances when it returns them.
    The ordinary namespace of this class gets a special function added into it
    called "init" that is used to create instances.
    This class can also be asked what member variables instances will have,
    which it works out by examining the var sections of its def_init method(s).
    """

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

