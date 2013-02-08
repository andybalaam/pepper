# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# From now on I will tell you of new things, of hidden things unknown to you.
# Isaiah 48 v6b

from pepinstance import PepInstance

class PepRuntimeInstance( PepInstance ):
    """
    An instance of a class that is not known at compile time - i.e. the
    construction code has been rendered in native code, and instances
    of this class allow us to track and render later calls to its methods
    (which is why we must hold the variable name).
    """

    def __init__( self, clazz, var_name ):
        PepInstance.__init__( self, clazz )
        self.var_name = var_name

    def construction_args( self ):
        return ( self.clazz, self.var_name )

    def is_known( self, env ):
        return False

