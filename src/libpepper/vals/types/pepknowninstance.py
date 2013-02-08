# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# You have searched me, Lord, and you know me.  Psalm 139 v1

from pepinstance import PepInstance

class PepKnownInstance( PepInstance ):
    """
    An instance of a class whose value is known at compile time.
    """

    def construction_args( self ):
        return ( self.clazz )

    def is_known( self, env ):
        return True

