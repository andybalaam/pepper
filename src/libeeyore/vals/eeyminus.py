from libeeyore.values import EeyBinaryOp

class EeyMinus( EeyBinaryOp ):
    def operator( self, lv, rv ):
        return lv.minus( rv )

