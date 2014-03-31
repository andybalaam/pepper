# Copyright (C) 2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# My tears have been my food day and night, while people say to me all
# day long, "Where is your God?"
# Psalm 42 v3

from libpepper.utils.execution_environment import execution_environment
from libpepper.usererrorexception import PepUserErrorException
from libpepper.values import PepBool
from libpepper.values import PepValue
from libpepper.values import pep_none

class PepWhile( PepValue ):
    def __init__( self, expression, body_stmts ):
        PepValue.__init__( self )
        self.expression = expression
        self.body_stmts = body_stmts

    def construction_args( self ):
        return (
            self.expression,
            self.body_stmts
        )

    def do_evaluate( self, env ):
        if self.expression.evaluated_type( env ).underlying_class() != PepBool:
            raise PepUserErrorException(
                "The expression used in a while loop must be Boolean." )

        # TODO: loops evaluate things multiple times - we must properly
        #       evaluate them again.  Here we hack them so they are always
        #       re-evaluated.
        #       Maybe all that's needed is an unevaluate() method that
        #       recursively sets cached_eval to None for you and all
        #       children?
        #       This all applies to for too, and probably other places

        expr = self.expression.evaluate( env )
        if expr.is_known( env ):
            while expr.value:
                for stmt in self.body_stmts:
                    stmt.cached_eval = None
                    ev_st = stmt.evaluate( env )
                    # TODO: handle return from inside for
                    #if ev_st.__class__ == PepReturn:
                    #    return ev_st.value.evaluate( newenv )
                self.expression.cached_eval = None
                expr = self.expression.evaluate( env )
            return pep_none
        else:
            return self


