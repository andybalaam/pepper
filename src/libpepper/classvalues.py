# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from itertools import ifilter

from libpepper.environment import PepEnvironment
from libpepper.namespace import PepNamespace
from languagevalues import PepInit
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

INIT_METHOD_NAME = "init"
INIT_IMPL_NAME = "__init__"


class PepDefInit( PepDef ):
    def __init__( self, arg_types_and_names, body_stmts ):
        PepDef.__init__(
            self,
            PepType( PepVoid ),
            PepSymbol( INIT_IMPL_NAME ),
            arg_types_and_names,
            body_stmts
        )
        # TODO: check there is at least one arg
        # TODO: check first arg accepts this class?

    def construction_args( self ):
        return ( self.arg_types_and_names, self.body_stmts )

    def get_member_variables( self ):
        ret = []

        is_var = lambda stmt: stmt.__class__ == PepVar
        for var_stmt in ifilter( is_var, self.body_stmts ):
            for init_stmt in var_stmt.body_stmts:
                if init_stmt.__class__ != PepInit:
                    # Should not happen since this is defined in the syntax
                    # (but might change one day?)
                    raise PepUserErrorException(
                        "Var blocks may only contain initialisation statements"
                    )
                # TODO: handle expressions that evaluate to symbols
                nm = init_stmt.var_name.name()
                selfdot = self.self_var_name() + "."
                if not nm.startswith( selfdot ):
                    raise PepUserErrorException(
                        "Only members of this class should be initialised in " +
                        "var blocks.  '" + nm + "' does not start with '" +
                        selfdot + "', but it should."
                    )
                nm = nm[ len(selfdot): ]

                if len( nm ) == 0:
                    raise PepUserErrorException(
                        "You must provide a variable name, not just '" +
                        selfdot + "'."
                    )

                ret.append( ( init_stmt.var_type, nm ) )

        return ret

    def self_var_name( self ):
        return self.arg_types_and_names[0][1].name()


class PepInstanceMethod( PepFunction ):
    def __init__( self, instance, fn ):
        PepFunction.__init__( self )
        self.instance = instance
        self.fn = fn

    def construction_args( self ):
        return ( self.instance, self.fn )

    def _instance_plus_args( self, args ):
        return (self.instance,) + args

    def call( self, args, env ):
        if all_known( args + (self.instance,), env ):
            return self.fn.call( self._instance_plus_args( args ), env )
        else:
            return PepRuntimeUserFunction(
                self.fn,
                self._instance_plus_args( args ),
                self.instance.clazz.name
            )

    def return_type( self, args, env ):
        return self.fn.return_type( self._instance_plus_args( args ), env )

    def args_match( self, args, env ):
        return self.fn.args_match( self._instance_plus_args( args ), env )

    def is_known( self, env ):
        return self.instance.is_known( env )


class PepInstanceNamespace( PepNamespace ):
    def __init__( self, instance, class_namespace ):
        PepNamespace.__init__( self )
        self.instance = instance
        self.class_namespace = class_namespace

    def _find( self, key ):

        found = PepNamespace._find( self, key)
        if found is not None:
            return found

        found = self.class_namespace._find( key )
        if isinstance( found, PepFunctionOverloadList ):
            return PepFunctionOverloadList(
                map(
                    lambda fn: PepInstanceMethod( self.instance, fn ),
                    found._list
                )
            )
        else:
            return found

class PepInstance( PepValue ):
    def __init__( self, clazz ):
        PepValue.__init__( self )
        self.clazz = clazz
        self.namespace = PepInstanceNamespace(
            self, self.clazz.get_namespace() )

    def get_class_name( self ):
        return self.clazz.name

    def get_namespace( self ):
        return self.namespace

    def evaluated_type( self, env ):
        return self.clazz


class PepKnownInstance( PepInstance ):
    def construction_args( self ):
        return ( self.clazz )

    def is_known( self, env ):
        return True

class PepRuntimeInstance( PepInstance ):
    def __init__( self, clazz, var_name ):
        PepInstance.__init__( self, clazz )
        self.var_name = var_name

    def construction_args( self ):
        return ( self.clazz, self.var_name )

    def is_known( self, env ):
        return False


class PepRuntimeInit( PepValue ):
    def __init__( self, instance, args, init_fn ):
        PepValue.__init__( self )
        # TODO: check arg types
        self.instance = instance
        self.args = args
        self.init_fn = init_fn

    def construction_args( self ):
        return ( self.instance, self.args, self.init_fn )

    def evaluated_type( self, env ):
        return self.instance.clazz

    def is_known( self, env ):
        return False



class PepInitMethod( PepFunction ):
    def __init__( self, user_class ):
        PepFunction.__init__( self )
        self.user_class = user_class

    def call( self, args, env ):
        if all_known( args, env ):
            ret = self.user_class.known_instance()
            if INIT_IMPL_NAME in self.user_class.namespace:
                self.user_class.namespace[INIT_IMPL_NAME].call(
                    (ret,) + args, env )
            # TODO: else default constructor
            return ret
        else:
            inst = self.user_class.runtime_instance( "" )
            return PepRuntimeInit(
                inst,
                args,
                self.user_class.namespace[INIT_IMPL_NAME].call(
                    (inst,) + args, env )
            )

    def return_type( self, args, env ):
        return self.user_class

    def args_match( self, args ):
        if INIT_IMPL_NAME not in self.user_class.namespace:
            # If there is no __init__, we will supply an empty constructor
            return ( len( args ) == 0 )

        # Make an object that looks like an instance so it passes the
        # call to matches() on the PepUserClass, and put it on the beginning
        # of the args array before we match against the user-defined init
        # method.
        self_plus_args = [ PepKnownInstance( self.user_class ) ] + args

        return self.user_class.namespace[INIT_IMPL_NAME].args_match(
            self_plus_args )

    def construction_args( self ):
        return ( self.user_class, )


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

class PepVar( PepValue ):
    def __init__( self, body_stmts ):
        PepValue.__init__( self )
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.body_stmts, )

    def do_evaluate( self, env ):
        for stmt in self.body_stmts:
            stmt.evaluate( env )
        return self

