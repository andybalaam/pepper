# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Men of understanding declare, wise men who hear me say to me, "Job speaks
# without knowledge; his words lack insight.  Job 34 v34-35

from libpepper.values import PepValue

from pepuserclass import PepUserClass

class PepClass( PepValue ):
    """
    The value created when a class is found in the source code.
    When evaluated, puts a PepUserClass into the namespace under the
    supplied name.
    """

    def __init__( self, name, base_classes, body_stmts ):
        PepValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def do_evaluate( self, env ):

        nm = self.name.name()

        if nm in env.namespace:
            raise PepUserErrorException(
                "The symbol '%s' is already defined." % nm )
             # TODO: line, column, filename
        else:
            env.namespace[nm] = PepUserClass(
                nm, self.base_classes, self.body_stmts )

        return self

    def check_init_matches( self, var_names ):
        pass # TODO: ensure later def_inits match the first one

