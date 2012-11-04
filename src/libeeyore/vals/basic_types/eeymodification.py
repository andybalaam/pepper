from libeeyore.values import EeyValue

class EeyModification( EeyValue ):
    def __init__( self, var_name, init_value ):
        EeyValue.__init__( self )
        self.var_name = var_name
        self.init_value = init_value

    def construction_args( self ):
        return ( self.var_name, self.init_value, )

