
from libeeyore.environment import EeyEnvironment
from libeeyore.namespace import EeyNamespace
from values import EeyValue

class EeyAbstractClass( EeyValue ):

    def __init__( self ):
        EeyValue.__init__( self )

    def is_known( self, env ):
        return True


class EeyUserClass( EeyAbstractClass ):
    def __init__( self, name, base_classes, body_stmts ):
        EeyAbstractClass.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts
        assert( len( self.body_stmts ) > 0 ) # TODO: not just assert

    def do_evaluate( self, env ):
        self.namespace = EeyNamespace( env.namespace )
        env = EeyEnvironment( env, self.namespace )
        for st in self.body_stmts:
            st.evaluate( env )
        return self

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )


class EeyClass( EeyValue ):
    def __init__( self, name, base_classes, body_stmts ):
        EeyValue.__init__( self )
        self.name = name
        self.base_classes = base_classes
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.name, self.base_classes, self.body_stmts )

    def do_evaluate( self, env ):

        nm = self.name.name()

        if nm in env.namespace:
            raise EeyUserErrorException(
                 "The symbol '%s' is already defined." % nm
             )
             # TODO: line, column, filename
        else:
            env.namespace[nm] = EeyUserClass(
                nm, self.base_classes, self.body_stmts )

        return self

class EeyVar( EeyValue ):
    def __init__( self, body_stmts ):
        self.body_stmts = body_stmts

    def construction_args( self ):
        return ( self.body_stmts, )
