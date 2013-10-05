# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# He has walled me in so that I cannot escape; he has weighed me down
# with chains.  Lamentations 3 v7

from itertools import izip

from libpepper.usererrorexception import PepUserErrorException
from libpepper.vals.functions.pepcallable import PepCallable
from libpepper.values import all_known
from libpepper.values import PepValue

def type_matches( env, tp, val ):
    return tp.evaluate( env ).matches( val.evaluated_type( env ), env )



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

    def signature_matches( self, ret_type, arg_types_and_names, env ):
        for fn in reversed( self._list ):
            if fn.signature_matches( ret_type, arg_types_and_names, env ):
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


