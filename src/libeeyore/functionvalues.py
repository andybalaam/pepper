from abc import ABCMeta
from abc import abstractmethod
from itertools import izip

from environment import EeyEnvironment
from values import EeySymbol
from values import EeyType
from values import EeyValue
from values import EeyVariable
from values import EeyPass
from values import all_known
from usererrorexception import EeyUserErrorException

def is_callable( value ):
    return True # TODO: check whether the object may be called

class EeyFunctionCall( EeyValue ):
    def __init__( self, func, args ):
        EeyValue.__init__( self )
        if func.__class__ == EeySymbol: # TODO: evaluate first?
            self.func_name = func.symbol_name
        else:
            self.func_name = None

        self.func = func
        self.args = args

    def construction_args( self ):
        return ( self.func, self.args )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            fn = self.func.evaluate( env )
            assert is_callable( fn ) # TODO: not assert
            return fn.call( env, self.args )
        else:
            return self

    def is_known( self, env ):
        return all_known( self.args, env )

    def evaluated_type( self, env ):
        return self.func.evaluate( env ).return_type()

class EeyReturn( EeyValue ):
    def __init__( self, value ):
        EeyValue.__init__( self )
        self.value = value

    def construction_args( self ):
        return ( self.value, )

class EeyCallable( EeyValue ):
    @abstractmethod
    def call( self, env, args ): pass

class EeyFunction( EeyCallable ):
    __metaclass__ = ABCMeta

    def __init__( self ):
        EeyValue.__init__( self )
#        self.arg_types_and_names = arg_types_and_names

    @abstractmethod
    def return_type( self ): pass

    @abstractmethod
    def args_match( self, args ): pass # TODO: move into EeyCallable

    def is_known( self, env ):
        return True

class EeyFunctionOverloadList( EeyCallable ):
    def __init__( self, first_fn ):
        EeyValue.__init__( self )
        self._list = [first_fn]

    def construction_args( self ):
        return ()

    def append( self, fn ):
        self._list.append( fn )

    def call( self, env, args ):
        assert( len( self._list ) > 0 )

        for fn in reversed( self._list ):
            if fn.args_match( env, args ):
                return fn.call( env, args )

        # If we got here, no overload matched
        if len( self._list ) == 1:
            # Special error if there was only one overload
            self.args_dont_match_error( self._list[0], env, args )
        else:
            self.no_match_error( env, args )

    def args_dont_match_error( self, fn, env, args ):
        if len( args ) != len( fn.arg_types_and_names ):
            raise EeyUserErrorException(
                ( "Wrong number of arguments to function {fn_name}.  " +
                    "You supplied {supplied}, but there should be {required}."
                ).format(
                    fn_name = fn.name,
                    supplied = len( args ),
                    required = len( fn.arg_types_and_names ),
                )
            )
            # TODO: line, col, file

        for argnum, ( arg, (reqtype, reqname) ) in enumerate( izip( args,
                fn.arg_types_and_names ) ):
            ev_reqtype = reqtype.evaluate( env )
            arg_type = arg.evaluated_type( env )

            if not ev_reqtype.matches( arg_type ):
                raise EeyUserErrorException(
                    ( "For function '{fn_name}', argument " +
                        "'{argname}' should be {reqtype}, " +
                        "not {supplied_type}."
                    ).format(
                        fn_name       = fn.name,
                        reqtype       = env.pretty_name( ev_reqtype ),
                        argname       = reqname.symbol_name,
                        supplied_type = env.pretty_name( arg_type ),
                    )
                )

        assert False, "args_dont_match_error called when the args do match!"

    def no_match_error( self, env, args ):
        def type_plus_arg( arg ):
            assert "value" in arg.__dict__, (
                "We don't support rendering unusual values nicely yet" ) #TODO

            return (
                env.pretty_name( arg.evaluated_type( env ) ) +
                " " + arg.value ) # TODO: render value nicely e.g. quoted

        supplied_args = "(%s)" % (
            ", ".join( type_plus_arg( arg ) for arg in args )
            )

        def type_and_arg( type_and_name ):
            return (
                env.pretty_name( type_and_name[0].evaluate( env ) ) +
                " " +
                type_and_name[1].symbol_name
            )

        def types_and_args( arg_types_and_names ):
            return ", ".join( type_and_arg( tn ) for tn in arg_types_and_names )

        overloads = (
            "\n".join(
                "(" + types_and_args( fn.arg_types_and_names ) + ")"
                    for fn in self._list
            )
        )

        msg = (
            ( "No overload of function {function_name} matches " +
            "the supplied arguments.  You supplied:" +
            "\n{supplied_args}\nbut the only allowed argument " +
            "lists are:\n{overloads}\n" ).format(
                function_name = self._list[0].name, # Names will all be same
                supplied_args = supplied_args,
                overloads = overloads,
                )
            )

        raise EeyUserErrorException( msg )



class EeyRuntimeUserFunction( EeyValue ):
    def __init__( self, user_function, args ):
        EeyValue.__init__( self )
        # TODO: check arg types
        self.user_function = user_function
        self.args = args

    def construction_args( self ):
        return ( self.user_function, self.args )

class EeyUserFunction( EeyFunction ):
    def __init__( self, name, ret_type, arg_types_and_names, body_stmts ):
        EeyFunction.__init__( self )
        #EeyFunction.__init__( self, arg_types_and_names )
        self.name = name
        self.ret_type = ret_type
        self.arg_types_and_names = arg_types_and_names
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert

    def construction_args( self ):
        return ( self.name, self.ret_type, self.arg_types_and_names,
            self.body_stmts )

    def return_type( self ):
        return self.ret_type

    def args_match( self, env, args ):
        if len( args ) != len( self.arg_types_and_names ):
            return False

        for arg, (reqtype, reqname) in izip( args, self.arg_types_and_names ):
            evald_req = reqtype.evaluate( env )
            arg_type = arg.evaluated_type( env )

            if not evald_req.matches( arg_type ):
                return False

        return True

    def call( self, env, args ):
        """You  must call args_match first and only call this if the return
        value was True"""
        if all_known( args, env ):

            newenv = self.execution_environment( env, args, True )

            for stmt in self.body_stmts:
                ev_st = stmt.evaluate( newenv )
                if ev_st.__class__ == EeyReturn:
                    return ev_st.value.evaluate( newenv )
            return EeyPass()
        else:
            return EeyRuntimeUserFunction( self, args )

    def execution_environment( self, env, args, known ):
        newenv = env.clone_deeper()

        for val, (tp, name) in izip( args, self.arg_types_and_names ):
            if known:
                val = val.evaluate( env )
            else:
                val = EeyVariable( tp.evaluate( env ) )
            newenv.namespace[name.name()] = val

        return newenv

class EeyDef( EeyValue ):
    def __init__( self, ret_type, name, arg_types_and_names, body_stmts ):
        EeyValue.__init__( self )
        self.ret_type = ret_type
        self.name = name
        self.arg_types_and_names = arg_types_and_names
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.ret_type, self.name, self.arg_types_and_names,
            self.body_stmts )

    def do_evaluate( self, env ):
        # TODO: should overloads only be allowed if we explicitly say
        #       def(overload)?
        # TODO: is it an error to overload with exactly the same type?
        # TODO: is it an error to overload with a different number of args?

        nm = self.name.name()

        fn = EeyUserFunction(
            nm, self.ret_type, self.arg_types_and_names, self.body_stmts )

        if nm in env.namespace:
            val = env.namespace[nm]

            if val.__class__ is not EeyFunctionOverloadList:
                raise EeyUserErrorException(
                    "The symbol '%s' is already defined." % nm
                )
                # TODO: line, column, filename

            val.append( fn )

        else:
            env.namespace[nm] = EeyFunctionOverloadList( fn )

        return self


