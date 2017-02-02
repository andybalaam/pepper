# Copyright (C) 2012-2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepValue

class PepTuple( PepValue ):
    def __init__( self, items ):
        PepValue.__init__( self )
        self.items = items

    def construction_args( self ):
        return ( self.items, )

    def do_evaluate( self, env ):
        return PepTuple( tuple( item.evaluate( env ) for item in self.items ) )

