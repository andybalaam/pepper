# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Peter replied, 'Even if all fall away on account of you, I never will.'
# Matt 26 v33

from libpepper.values import PepValue

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

#    def do_evaluate( self, env ):
#
#        nm = self.name.name()
#
#        fn = PepUserInterfaceFunction(
#            nm,
#            self.ret_type.evaluate( env ),
#            self.arg_types_and_names
#        ).evaluate( env )
#
#        if nm in env.namespace:
#            val = env.namespace[nm]
#
#            assert( val.__class__ is PepFunctionOverloadList )
#
#            val.append( fn )
#
#        else:
#            env.namespace[nm] = PepFunctionOverloadList( [fn] )
#
#        return self
#
    pass

