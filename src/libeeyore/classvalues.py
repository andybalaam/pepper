
from libeeyore.environment import EeyEnvironment
from libeeyore.namespace import EeyNamespace
from values import EeyTypeMatcher
from values import EeySymbol
from values import EeyValue
from functionvalues import EeyFunction
from functionvalues import EeyDef
from usererrorexception import EeyUserErrorException

INIT_METHOD_NAME = "init"
INIT_IMPL_NAME = "__init__"


class EeyDefInit( EeyDef ):
    def __init__( self, arg_types_and_names, body_stmts ):
        EeyDef.__init__(
            self,
            None,
            EeySymbol( INIT_IMPL_NAME ),
            arg_types_and_names,
            body_stmts
        )

    def construction_args( self ):
        return ( self.arg_types_and_names, self.body_stmts )

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

class FakeInstance( EeyInstance ):
    def __init__( self, clazz ):
        self.clazz = clazz

class EeyInitMethod( EeyFunction ):
    def __init__( self, user_class ):
        EeyFunction.__init__( self )
        self.user_class = user_class

    def call( self, env, args ):
        ret = self.user_class.create_instance()
        if INIT_IMPL_NAME in self.user_class.namespace:
            self.user_class.namespace[INIT_IMPL_NAME].call(
                env, (ret,) + args )
        return ret

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

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def create_instance( self ):
        return EeyInstance( self )

    def matches( self, value_type ):
        """
        @return True if the value_type supplied is this class.
        """
        return ( value_type == self )


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

class EeyVar( EeyValue ):
    def __init__( self, body_stmts ):
        EeyValue.__init__( self )
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.body_stmts, )

    def do_evaluate( self, env ):
        for stmt in self.body_stmts:
            stmt.evaluate( env )

