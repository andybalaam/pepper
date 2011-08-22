
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
            builtinmodules.eeysys.add_names( env )
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
    def __init__( self, predicate, cmds_if_true ):
        EeyValue.__init__( self )
        self.predicate = predicate
        self.cmds_if_true = cmds_if_true

    def construction_args( self ):
        return ( self.predicate, self.cmds_if_true )

    def do_evaluate( self, env ):
        pred = self.predicate.evaluate( env )
        if pred.is_known( env ):
            assert( pred.__class__ == EeyBool ) # TODO: other types
            if pred.value:
                # TODO: support EeyArray of statements?  As well?
                ret = None
                for cmd in self.cmds_if_true:
                    ret = cmd.evaluate( env )
                return ret # TODO: should we return all evaluated statements?
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

        nm = self.var_name # Don't evaluate - will need to semi-evaluate in
                           # order to support symbol( "x" ) here?
        assert( nm.__class__ == EeySymbol ) # TODO: not assert

        val = self.init_value.evaluate( env )

        return ( tp, nm, val )

    def do_evaluate( self, env ):
        ( tp, nm, val ) = self._eval_args( env )

        assert( nm.symbol_name not in env.namespace ) # TODO: not assert

        if self.is_known( env ):
            if tp.value != val.__class__:
                raise EeyInitialisingWithWrongType(
                    tp, val.__class__ )

            env.namespace[nm.symbol_name] = val
        else:
            if tp.value != val.evaluated_type( env ):
                raise EeyInitialisingWithWrongType(
                    tp, val.evaluated_type( env ) )
            env.namespace[nm.symbol_name] = EeyVariable( tp.value )

        return self

    def is_known( self, env ):
        ( tp, nm, val ) = self._eval_args( env )
        return all_known( ( tp, val ), env )


