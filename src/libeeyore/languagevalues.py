
from all_known import all_known
from eeyinterface import implements_interface
from values import EeyArray
from values import EeyInt
from values import EeyValue

from usererrorexception import EeyUserErrorException

class EeyImport( EeyValue ):
    def __init__( self, module_name ):
        self.module_name = module_name

    def construction_args( self ):
        return ( self.module_name, )

    def evaluate( self, env ):
        if self.module_name == "sys":
            import builtinmodules.eeysys
            builtinmodules.eeysys.add_names( env )
        else:
            raise EeyUserErrorException( "No module named %s" %
                self.module_name )
        return self


class EeyArrayLookup( EeyValue ):
    def __init__( self, array_value, index ):
        self.array_value = array_value
        self.index = index

    def construction_args( self ):
        return ( self.array_value, self.index )

    def evaluate( self, env ):
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
        self.predicate = predicate
        self.cmds_if_true = cmds_if_true

    def construction_args( self ):
        return ( self.predicate, self.cmds_if_true )

    def evaluate( self, env ):
        pred = self.predicate.evaluate( env )
        if pred.is_known( env ):
            assert( idx.__class__ == EeyBool ) # TODO: other types
            if pred.value:
                # TODO: support EeyArray of statements?  As well?
                ret = None
                for cmd in self.cmds_if_true:
                    ret = cmd.evaluate( env )
                return ret # TODO: should we return all evaluated statements?
            else:
                return EeyBool( "False" )
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

