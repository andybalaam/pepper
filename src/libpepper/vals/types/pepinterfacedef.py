# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Peter replied, 'Even if all fall away on account of you, I never will.'
# Matt 26 v33

from libpepper.values import PepValue
from libpepper.values import PepPass
from libpepper.functionvalues import PepFunctionOverloadList
from libpepper.vals.functions.pepuserfunction import PepUserFunction

class PepInterfaceDef( PepValue ):
    """
    The value created when a def within an interface is parsed.
    Allows specifying a method signature that must be found within a type
    if it matches the containing interface.
    """

    def __init__( self, ret_type, name, arg_types_and_names ):
        PepValue.__init__( self )
        self.ret_type = ret_type
        self.name = name
        self.arg_types_and_names = arg_types_and_names

    def construction_args( self ):
        return ( self.ret_type, self.name, self.arg_types_and_names )

    def do_evaluate( self, env ):
        nm = self.name.name()

        fn = PepUserFunction(
            nm,
            self.ret_type.evaluate( env ),
            self.arg_types_and_names,
            ( PepPass(), )
        ).evaluate( env )

        # TODO: share code with PepDef

        env.namespace[nm] = PepFunctionOverloadList( [fn] )

        return self

