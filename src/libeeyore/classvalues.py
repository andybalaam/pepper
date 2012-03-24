from values import EeyValue

class EeyClass( EeyValue ):
    def __init__( self, name, base_classes, body_stmts ):
        EeyValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def do_evaluate( self, env ):

#        nm = self.name.name()
#
#        fn = EeyUserFunction(
#            nm, self.ret_type, self.arg_types_and_names, self.body_stmts )
#
#        if nm in env.namespace:
#            val = env.namespace[nm]
#
#            if val.__class__ is not EeyFunctionOverloadList:
#                raise EeyUserErrorException(
#                    "The symbol '%s' is already defined." % nm
#                )
#                # TODO: line, column, filename
#
#            val.append( fn )
#
#        else:
#            env.namespace[nm] = EeyFunctionOverloadList( fn )
#
        return self

