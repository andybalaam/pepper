
from all_known import all_known
from eeyinterface import implements_interface
from values import EeyArray
from values import EeyBool
from values import EeyInt
from values import EeySymbol
from values import EeyType
from values import EeyValue
from values import EeyVariable
from values import eey_none

from usererrorexception import EeyUserErrorException

class EeyImport( EeyValue ):
    def __init__( self, module_name ):
        EeyValue.__init__( self )
        self.module_name = module_name

    def construction_args( self ):
        return ( self.module_name, )

    def do_evaluate( self, env ):

        if self.module_name == "sys":
            import builtinmodules.eeysys
            env.namespace["sys"] = builtinmodules.eeysys.EeySys()
        else:
            raise EeyUserErrorException( "No module named %s" %
                self.module_name )

        self.cached_eval = self
        return self


class EeyArrayLookup( EeyValue ):
    def __init__( self, array_value, index ):
        EeyValue.__init__( self )
        self.array_value = array_value
        self.index = index

    def construction_args( self ):
        return ( self.array_value, self.index )

    def do_evaluate( self, env ):
        idx = self.index.evaluate( env )
        arr = self.array_value.evaluate( env )
        if arr.is_known( env ):
            assert( idx.__class__ == EeyInt )
            assert( implements_interface( arr, EeyArray ) )
            # TODO: handle large number indices
            return arr.get_index( int( idx.value ) ).evaluate( env )
        else:
            return self

    def is_known( self, env ):
        return all_known( ( self.array_value, self.index ), env )

class EeyIf( EeyValue ):
    def __init__( self, predicate, cmds_if_true, cmds_if_false ):
        EeyValue.__init__( self )
        self.predicate = predicate
        self.cmds_if_true = cmds_if_true
        self.cmds_if_false = cmds_if_false

    def construction_args( self ):
        return ( self.predicate, self.cmds_if_true, self.cmds_if_false )

    def do_evaluate( self, env ):
        pred = self.predicate.evaluate( env )
        if pred.is_known( env ):
            assert( pred.__class__ == EeyBool ) # TODO: other types
            if pred.value:
                return self._run_commands( self.cmds_if_true, env )
            elif self.cmds_if_false is not None:
                return self._run_commands( self.cmds_if_false, env )
            else:
                return eey_none
        else:
            return self

    def is_known( self, env ):
        pred = self.predicate.evaluate( env )
        return ( pred.is_known( env ) and (
                ( pred.value and all_known( self.cmds_if_true ) )
                or
                ( not pred.value ) # TODO and elses known)
                )
            )

    def _run_commands( self, cmds, env ):
        # TODO: support EeyArray of statements?  As well?
        ret = None
        for cmd in cmds:
            ret = cmd.evaluate( env )
        return ret # TODO: should we return all evaluated statements?

class EeyInitialisingWithWrongType( EeyUserErrorException ):
    def __init__( self, decl_type, init_value_type ):
        EeyUserErrorException.__init__( self, ( "Declared type is %s, but "
            + "initial value supplied is of type %s." ) % (
                str( decl_type ), str( init_value_type )
                ) )

class EeyInit( EeyValue ):

    def __init__( self, var_type, var_name, init_value ):
        EeyValue.__init__( self )
        self.var_type   = var_type
        self.var_name   = var_name
        self.init_value = init_value

    def construction_args( self ):
        return ( self.var_type, self.var_name, self.init_value )

    def _eval_args( self, env ):
        tp = self.var_type.evaluate( env )

        # Don't evaluate - will need to semi-evaluate in
        # order to support symbol( "x" ) here?
        assert( self.var_name.__class__ == EeySymbol ) # TODO: not assert
        (namespace, name, base_sym) = self.var_name.find_namespace_and_name(
            env )

        val = self.init_value.evaluate( env )

        return ( tp, namespace, name, val )

    def do_evaluate( self, env ):
        ( tp, ns, nm, val ) = self._eval_args( env )

        if nm in ns:
            raise EeyUserErrorException(
                "Namespace already contains the name '" + nm + "'." )

        val_type = val.evaluated_type( env )
        if not tp.matches( val_type ):
            raise EeyInitialisingWithWrongType( tp, val_type )

        def make_value():
            if val.is_known( env ):
                return val
            else:
                return EeyVariable( tp )

        ns[nm] = make_value()

        return self

    def is_known( self, env ):
        ( tp, ns, nm, val ) = self._eval_args( env )
        return all_known( ( tp, val ), env )


