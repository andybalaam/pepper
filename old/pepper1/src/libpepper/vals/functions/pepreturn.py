# Copyright (C) 2011-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepValue

class PepReturn( PepValue ):
    def __init__( self, value ):
        PepValue.__init__( self )
        self.value = value

    def construction_args( self ):
        return ( self.value, )

    def do_evaluate( self, env ):
        return PepReturn( self.value.evaluate( env ) )

