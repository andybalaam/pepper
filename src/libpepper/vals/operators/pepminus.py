# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from libpepper.values import PepBinaryOp

class PepMinus( PepBinaryOp ):
    def operator( self, lv, rv ):
        return lv.minus( rv )

