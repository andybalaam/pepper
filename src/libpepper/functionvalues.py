# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from abc import ABCMeta
from abc import abstractmethod
from itertools import izip

from environment import PepEnvironment
from values import PepSymbol
from values import PepType
from values import PepValue
from values import PepVariable
from values import PepPass
from values import all_known
from usererrorexception import PepUserErrorException



def has_default( type_and_name ):
    return ( len( type_and_name ) == 3 )

def type_matches( env, tp, val ):
    return tp.evaluate( env ).matches( val.evaluated_type( env ) )


def execution_environment( arg_types_and_names, args, known, env ):
    newenv = env.clone_deeper()

    i = 0
    while i < len( arg_types_and_names ):
        type_and_name = arg_types_and_names[i]
        name = type_and_name[1]

        if i < len( args ):
            val = args[i]
        else:
            assert has_default( type_and_name )
            val = type_and_name[2]

        if known:
            val = val.evaluate( env )
        else:
            tp   = type_and_name[0]
            val = PepVariable( tp.evaluate( env ), name.name() )

        newenv.namespace[name.name()] = val
        i += 1

    return newenv


def is_callable( value ):
    return True # TODO: check whether the object may be called

class PepFunctionCall( PepValue ):
    def __init__( self, func, args ):
        PepValue.__init__( self )
        if func.__class__ == PepSymbol: # TODO: evaluate first?
            self.func_name = func.symbol_name
        else:
            self.func_name = None

        self.func = func
        self.args = args

    def construction_args( self ):
        return ( self.func, self.args )

    def do_evaluate( self, env ):
        fn = self.func.evaluate( env )
        assert is_callable( fn ) # TODO: not assert
        return fn.call( self.args, env )

    def is_known( self, env ):
        return all_known( self.args + (self.func,), env )

    def evaluated_type( self, env ):
        return self.func.evaluate( env ).return_type( self.args, env )

class PepReturn( PepValue ):
    def __init__( self, value ):
        PepValue.__init__( self )
        self.value = value

    def construction_args( self ):
        return ( self.value, )

    def do_evaluate( self, env ):
        return PepReturn( self.value.evaluate( env ) )

class PepCallable( PepValue ):
    @abstractmethod
    def call( self, args, env ): pass

    @abstractmethod
    def return_type( self, args, env ): pass

    @abstractmethod
    def args_match( self, args, env ): pass

class PepFunction( PepCallable ):
    __metaclass__ = ABCMeta

    def __init__( self ):
        PepValue.__init__( self )
#        self.arg_types_and_names = arg_types_and_names

    def is_known( self, env ):
        return True

class PepFunctionOverloadList( PepCallable ):
    def __init__( self, initial_list ):
        PepValue.__init__( self )
        self._list = initial_list

    def is_known( self, env ):
        return all_known( self._list, env )

    def construction_args( self ):
        return ()

    def append( self, fn ):
        self._list.append( fn )

    def return_type( self, args, env ):
        return self._get_fn( args, env ).return_type( args, env )

    def _get_fn( self, args, env ):
        for fn in reversed( self._list ):
            if fn.args_match( args, env ):
                return fn

        return None

    def args_match( self, args, env ):
        return ( self._get_fn( args, env ) is not None )

    def signature_matches( self, ret_type, arg_types_and_names ):
        for fn in reversed( self._list ):
            if fn.signature_matches( ret_type, arg_types_and_names ):
                return True
        return False

    def call( self, args, env ):
        assert( len( self._list ) > 0 )

        matching_fn = self._get_fn( args, env )
        if matching_fn is not None:
            return matching_fn.call( args, env )

        # If we got here, no overload matched
        if len( self._list ) == 1:
            # Special error if there was only one overload
            self.args_dont_match_error( self._list[0], args, env )
        else:
            self.no_match_error( args, env )

    def args_dont_match_error( self, fn, args, env ):
        if len( args ) != len( fn.arg_types_and_names ):
            raise PepUserErrorException(
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

            if not type_matches( env, reqtype, arg ):
                ev_reqtype = reqtype.evaluate( env )
                arg_type = arg.evaluated_type( env )
                raise PepUserErrorException(
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

    def no_match_error( self, args, env ):
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

        raise PepUserErrorException( msg )



class PepRuntimeUserFunction( PepValue ):
    def __init__( self, user_function, args, namespace_name ):
        PepValue.__init__( self )
        # TODO: check arg types
        self.user_function = user_function
        self.args = args
        self.namespace_name = namespace_name

    def construction_args( self ):
        return ( self.user_function, self.args, self.namespace_name )

    def is_known( self, env ):
        return False

    def evaluated_type( self, env ):
        return self.user_function.return_type( self.args, env )


class PepUserFunction( PepFunction ):
    def __init__( self, name, ret_type, arg_types_and_names, body_stmts ):
        PepFunction.__init__( self )
        #PepFunction.__init__( self, arg_types_and_names )
        self.name = name
        self.ret_type = ret_type
        self.arg_types_and_names = arg_types_and_names
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert

    def construction_args( self ):
        return ( self.name, self.ret_type, self.arg_types_and_names,
            self.body_stmts )

    def return_type( self, args, env ):
        return self.ret_type

    def do_evaluate( self, env ):
        self.check_default_arg_types( env )
        return self

    def check_default_arg_types( self, env ):
        for type_and_name in self.arg_types_and_names:
            if has_default( type_and_name ):
                if not type_matches( env, type_and_name[0], type_and_name[2] ):
                    reqtype = type_and_name[0].evaluate( env )
                    deftype = type_and_name[2].evaluated_type( env )
                    raise PepUserErrorException(
                        (
                            "In function '{funcname}', the default for " +
                            "argument '{argname}' should be {reqtype}, but " +
                            "it is {deftype}."
                        ).format(
                            funcname = self.name,
                            argname = type_and_name[1].symbol_name,
                            reqtype = env.pretty_name( reqtype ),
                            deftype = env.pretty_name( deftype ),
                        )
                    )

    def args_match( self, args, env ):

        i = 0
        while True:

            # Have we looked at all allowed args?  Then we're finished
            if i >= len( self.arg_types_and_names ):
                # Matches if we've finished all the args too
                return ( i >= len( args ) )

            type_and_name = self.arg_types_and_names[i]

            # Have we run out of args?  If so, remaining allowed must be opt
            if i >= len( args ):
                if not has_default( type_and_name ):
                    return False
            else:
                if not type_matches( env, type_and_name[0], args[i] ):
                    return False

            i += 1

    def signature_matches( self, ret_type, arg_types_and_names ):
        return (
            ret_type            == self.ret_type and
            arg_types_and_names == self.arg_types_and_names
        )

    def call( self, args, env ):
        """You  must call args_match first and only call this if the return
        value was True"""
        if all_known( args, env ):

            newenv = self.execution_environment( args, True, env )

            for stmt in self.body_stmts:
                ev_st = stmt.evaluate( newenv )
                if ev_st.__class__ == PepReturn:
                    return ev_st.value.evaluate( newenv )
            return PepPass()
        # TODO: if this is a pure function, could we partially-evaluate it?

        return PepRuntimeUserFunction( self, args, None )

    def execution_environment( self, args, known, env ):
        return execution_environment(
            self.arg_types_and_names, args, known, env )


class PepDef( PepValue ):
    def __init__( self, ret_type, name, arg_types_and_names, body_stmts ):
        PepValue.__init__( self )
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

        fn = PepUserFunction(
            nm,
            self.ret_type.evaluate( env ),
            self.arg_types_and_names,
            self.body_stmts
        ).evaluate( env )

        if nm in env.namespace:
            val = env.namespace[nm]

            if val.__class__ is not PepFunctionOverloadList:
                raise PepUserErrorException(
                    "The symbol '%s' is already defined." % nm
                )
                # TODO: line, column, filename

            val.append( fn )

        else:
            env.namespace[nm] = PepFunctionOverloadList( [fn] )

        return self


