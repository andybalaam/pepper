
from itertools import ifilter

from libeeyore.environment import EeyEnvironment
from libeeyore.namespace import EeyNamespace
from languagevalues import EeyInit
from values import EeyType
from values import EeyTypeMatcher
from values import EeySymbol
from values import EeyString
from values import EeyValue
from values import EeyVoid
from values import all_known
from functionvalues import EeyDef
from functionvalues import EeyFunction
from functionvalues import EeyRuntimeUserFunction
from usererrorexception import EeyUserErrorException

INIT_METHOD_NAME = "init"
INIT_IMPL_NAME = "__init__"


class EeyDefInit( EeyDef ):
    def __init__( self, arg_types_and_names, body_stmts ):
        EeyDef.__init__(
            self,
            EeyType( EeyVoid ),
            EeySymbol( INIT_IMPL_NAME ),
            arg_types_and_names,
            body_stmts
        )
        # TODO: check there is at least one arg
        # TODO: check first arg accepts this class?

    def construction_args( self ):
        return ( self.arg_types_and_names, self.body_stmts )

    def get_member_variables( self, env ):
        ret = []

        is_var = lambda stmt: stmt.__class__ == EeyVar
        for var_stmt in ifilter( is_var, self.body_stmts ):
            for init_stmt in var_stmt.body_stmts:
                if init_stmt.__class__ != EeyInit:
                    # Should not happen since this is defined in the syntax
                    # (but might change one day?)
                    raise EeyUserErrorException(
                        "Var blocks may only contain initialisation statements"
                    )
                # TODO: handle expressions that evaluate to symbols
                nm = init_stmt.var_name.name()
                selfdot = self.self_var_name() + "."
                if not nm.startswith( selfdot ):
                    raise EeyUserErrorException(
                        "Only members of this class should be initialised in " +
                        "var blocks.  '" + nm + "' does not start with '" +
                        selfdot + "', but it should."
                    )
                nm = nm[ len(selfdot): ]

                if len( nm ) == 0:
                    raise EeyUserErrorException(
                        "You must provide a variable name, not just '" +
                        selfdot + "'."
                    )

                ret.append( ( init_stmt.var_type, nm ) )

        return ret

    def self_var_name( self ):
        return self.arg_types_and_names[0][1].name()

class EeyInstance( EeyValue ):
    def __init__( self, clazz ):
        EeyValue.__init__( self )
        self.clazz = clazz
        self.namespace = EeyNamespace()

    def get_class_name( self ):
        return self.clazz.name

    def construction_args( self ):
        return ( self.clazz, )

    def evaluated_type( self, env ):
        return self.clazz


class EeyRuntimeInstance( EeyValue ):
    def __init__( self, instance, args, init_fn ):
        EeyValue.__init__( self )
        # TODO: check arg types
        self.instance = instance
        self.args = args
        self.init_fn = init_fn

    def construction_args( self ):
        return ( self.instance, self.args, self.init_fn )


class FakeInstance( EeyInstance ):
    def __init__( self, clazz ):
        self.clazz = clazz

class EeyInitMethod( EeyFunction ):
    def __init__( self, user_class ):
        EeyFunction.__init__( self )
        self.user_class = user_class

    def call( self, env, args ):
        if all_known( args, env ):
            ret = self.user_class.create_instance()
            if INIT_IMPL_NAME in self.user_class.namespace:
                self.user_class.namespace[INIT_IMPL_NAME].call(
                    env, (ret,) + args )
            # TODO: else default constructor
            return ret
        else:
            inst = self.user_class.create_instance()
            return EeyRuntimeInstance(
                inst,
                args,
                self.user_class.namespace[INIT_IMPL_NAME].call(
                    env, (inst,) + args )
            )

    def return_type( self ):
        return self.user_class

    def args_match( self, args ):
        if INIT_IMPL_NAME not in self.user_class.namespace:
            # If there is no __init__, we will supply an empty constructor
            return ( len( args ) == 0 )

        # Make an object that looks like an instance so it passes the
        # call to matches() on the EeyUserClass, and put it on the beginning
        # of the args array before we match against the user-defined init
        # method.
        self_plus_args = [ FakeInstance( self.user_class ) ] + args

        return self.user_class.namespace[INIT_IMPL_NAME].args_match(
            self_plus_args )

    def construction_args( self ):
        return ( self.user_class, )

class EeyUserClass( EeyValue, EeyTypeMatcher ):
    def __init__( self, name, base_classes, body_stmts ):
        EeyValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert
        self.namespace = None

    def is_known( self, env ):
        return True # TODO - not always known

    def do_evaluate( self, env ):
        self.namespace = EeyNamespace( env.namespace )
        subenv = EeyEnvironment( env.renderer, self.namespace )
        for st in self.body_stmts:
            st.evaluate( subenv )

        if INIT_METHOD_NAME in self.namespace:
            raise EeyUserErrorException( "You may not define the symbol " +
                "'%s' in a class definition." % INIT_METHOD_NAME )

        # TODO: disallow defining functions called __init__

        self.namespace[INIT_METHOD_NAME] = EeyInitMethod( self )

        return self

    def get_member_variables( self, env ):
        ret = []

        first_def_init = True
        is_def_init = lambda stmt: stmt.__class__ == EeyDefInit
        for stmt in ifilter( is_def_init, self.body_stmts ):
            if first_def_init:
                ret = stmt.get_member_variables( env )
            else:
                self.check_init_matches( ret )
            first_def_init = False

        return ret

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def create_instance( self ):
        return EeyInstance( self )

    def matches( self, other ):
        """
        @return True if other is this class.
        """
        return ( other == self )

    def get_name( self ):
        return self.name

    def underlying_class( self ):
        return self

class EeyClass( EeyValue ):
    def __init__( self, name, base_classes, body_stmts ):
        EeyValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def do_evaluate( self, env ):

        nm = self.name.name()

        if nm in env.namespace:
            raise EeyUserErrorException(
                "The symbol '%s' is already defined." % nm )
             # TODO: line, column, filename
        else:
            env.namespace[nm] = EeyUserClass(
                nm, self.base_classes, self.body_stmts )

        return self

    def check_init_matches( self, var_names ):
        pass # TODO: ensure later def_inits match the first one

class EeyVar( EeyValue ):
    def __init__( self, body_stmts ):
        EeyValue.__init__( self )
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.body_stmts, )

    def do_evaluate( self, env ):
        for stmt in self.body_stmts:
            stmt.evaluate( env )
        return self

