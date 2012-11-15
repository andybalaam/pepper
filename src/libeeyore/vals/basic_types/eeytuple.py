# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libeeyore.values import EeyValue

class EeyTuple( EeyValue ):
    def __init__( self, items ):
        EeyValue.__init__( self )
        self.items = items

    def construction_args( self ):
        return ( self.items, )

