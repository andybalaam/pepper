from libeeyore.values import EeyValue

class EeyFor( EeyValue ):
    def __init__( self, var_type, var_name, range_expr, body_stmts ):
        EeyValue.__init__( self )
        self.var_type = var_type
        self.var_name = var_name
        self.range_expr = range_expr
        self.body_stmts = body_stmts

    def construction_args( self ):
        return (
            self.var_type,
            self.var_name,
            self.range_expr,
            self.body_stmts
        )

