# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.environment import PepEnvironment
from libpepper.namespace import PepNamespace
from values import PepType

from values import PepSymbol
from values import PepString
from values import PepValue
from values import PepVariable
from values import PepVoid
from values import all_known
from functionvalues import PepCallable
from functionvalues import PepDef
from functionvalues import PepFunction
from functionvalues import PepFunctionOverloadList
from functionvalues import PepRuntimeUserFunction
from usererrorexception import PepUserErrorException
from vals.types import PepDefInit
from vals.types import PepInitMethod
from vals.types import PepInstanceMethod
from vals.types import PepInstanceNamespace
from vals.types import PepKnownInstance
from vals.types import PepRuntimeInit
from vals.types import PepRuntimeInstance
from vals.types import PepUserClass

class PepClass( PepValue ):
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

