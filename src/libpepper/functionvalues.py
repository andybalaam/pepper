# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from abc import ABCMeta
from abc import abstractmethod
from itertools import izip

from environment import PepEnvironment
from values import PepSymbol
from values import PepType
from values import PepValue
from vals.functions import PepUserFunction
from vals.functions import PepFunctionOverloadList
from values import PepPass
from values import all_known
from usererrorexception import PepUserErrorException


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
        if fn.is_known( env ):
            return fn.call( self.args, env )
        else:
            return self

    def is_known( self, env ):
        return all_known( self.args + (self.func,), env )

    def evaluated_type( self, env ):
        return self.func.evaluate( env ).return_type( self.args, env )


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


