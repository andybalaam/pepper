# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# For just as each of us has one body with many members, and these members do
# not all have the same function, so in Christ we, though many, form one body,
# and each member belongs to all the others.  Romans 12 v4-5

from libpepper.values import PepValue

class PepVar( PepValue ):
    """
    The value created when a var is found inside a def_init in source code.
    A var allows declaring and initialising data members of a class.  It may
    contain only initialisation statements of variables declared as e.g.
    "int self.mything = 4"
    """

    def __init__( self, body_stmts ):
        PepValue.__init__( self )
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.body_stmts, )

    def do_evaluate( self, env ):
        for stmt in self.body_stmts:
            stmt.evaluate( env )
        return self

