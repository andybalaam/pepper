# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.utils.execution_environment import execution_environment
from libpepper.values import PepValue
from libpepper.values import pep_none

class PepFor( PepValue ):
    def __init__(
            self, variable_type, variable_name, iterator, body_stmts ):
        PepValue.__init__( self )
        self.variable_type = variable_type
        self.variable_name = variable_name
        self.iterator = iterator
        self.body_stmts = body_stmts

    def construction_args( self ):
        return (
            self.variable_type,
            self.variable_name,
            self.iterator,
            self.body_stmts
        )

    def do_evaluate( self, env ):
        it = self.iterator.evaluate( env )
        if it.is_known( env ):
            for item in it:
                newenv = execution_environment(
                    ( ( self.variable_type, self.variable_name ), ),
                    ( item, ),
                    True,
                    env
                )
                for stmt in self.body_stmts:
                    ev_st = stmt.evaluate( newenv )
                    # TODO: handle return from inside for
                    #if ev_st.__class__ == PepReturn:
                    #    return ev_st.value.evaluate( newenv )
            return pep_none
        else:
            return self

