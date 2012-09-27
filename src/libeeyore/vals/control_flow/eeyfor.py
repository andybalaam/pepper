from libeeyore.values import EeyValue

class EeyFor( EeyValue ):
    def __init__(
            self, variable_type, variable_name, iterator, body_statements ):
        EeyValue.__init__( self )
        self.variable_type = variable_type
        self.variable_name = variable_name
        self.iterator = iterator
        self.body_statements = body_statements

    def construction_args( self ):
        return (
            self.variable_type,
            self.variable_name,
            self.iterator,
            self.body_statements
        )


