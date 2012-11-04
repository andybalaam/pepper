from libeeyore.values import EeyValue
from libeeyore.values import all_known

class EeyModification( EeyValue ):
    def __init__( self, var, mod_value ):
        EeyValue.__init__( self )
        self.var = var
        self.mod_value = mod_value

    def construction_args( self ):
        return ( self.var, self.mod_value, )

    def do_evaluate( self, env ):
        if self.is_known( env ):
            self.var.evaluate(
                env ).plusequals( self.mod_value.evaluate( env ) )
        return self

    def is_known( self, env ):
        return all_known( ( self.var, self.mod_value, ), env )



