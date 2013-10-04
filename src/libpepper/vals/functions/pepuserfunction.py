# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Your hands shaped me and made me. Will you now turn and destroy me?
# Job 10 v8

from libpepper.utils.execution_environment import execution_environment
from libpepper.values import all_known
from libpepper.values import PepPass

from pepfunction import PepFunction
from pepreturn import PepReturn
from pepruntimeuserfunction import PepRuntimeUserFunction

from libpepper.usererrorexception import PepUserErrorException

def _has_default( type_and_name ):
    return ( len( type_and_name ) == 3 )

def _type_matches( env, tp, val ):
    return tp.evaluate( env ).matches( val.evaluated_type( env ), env )

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
        # TODO: check the arguments are type-matchers
        self.check_default_arg_types( env )
        return self

    def check_default_arg_types( self, env ):
        for type_and_name in self.arg_types_and_names:
            if _has_default( type_and_name ):
                if not _type_matches( env, type_and_name[0], type_and_name[2] ):
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
                if not _has_default( type_and_name ):
                    return False
            else:
                if not _type_matches( env, type_and_name[0], args[i] ):
                    return False

            i += 1

    def signature_matches( self, ret_type, arg_types_and_names, env ):
        return (
            ret_type.evaluate( env ) == self.ret_type.evaluate( env ) and
            (
                tuple( a[0].evaluate( env ) for a in arg_types_and_names ) ==
                tuple( a[0].evaluate( env ) for a in self.arg_types_and_names )
            )
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

