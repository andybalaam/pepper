from libeeyore.values import EeyValue

class EeyModification( EeyValue ):
    def __init__( self, var, mod_value ):
        EeyValue.__init__( self )
        self.var = var
        self.mod_value = mod_value

    def construction_args( self ):
        return ( self.var, self.mod_value, )

    def do_evaluate( self, env ):
        self.var.evaluate( env ).plusequals( self.mod_value.evaluate( env ) )
        return self



