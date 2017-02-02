# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# a time to kill and a time to heal, a time to tear down and a time to build
# Ecclesiates 3 v3

from libpepper.values import PepValue

class PepRuntimeInit( PepValue ):
    """
    An object representing a call of an init method.  It will be rendered in
    the native code as a declaration and calling an initialisation function.
    """

    def __init__( self, instance, args, init_fn ):
        PepValue.__init__( self )
        # TODO: check arg types
        self.instance = instance
        self.args = args
        self.init_fn = init_fn

    def construction_args( self ):
        return ( self.instance, self.args, self.init_fn )

    def evaluated_type( self, env ):
        return self.instance.clazz

    def is_known( self, env ):
        return False

