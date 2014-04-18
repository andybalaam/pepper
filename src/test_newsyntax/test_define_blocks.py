from tools import *

class PepBlock( object ):
    def after( self, next_block ):
        """
            Take in the block following this one and return a new block.
            If the block after is the wrong type, throw ExpectedBlock.
            If we don't expect anything after us, return None.
            If we don't have to have anything after us, and the next
            block is a type we don't recognise, return None.
        """
        pass

    def unblock( self ):
        """
            Return a normal PepValue build from this block.
        """
        pass

#simple_block = PepFunctionCall( PepSymbol('foo'), [] )
#code_block = PepCodeBlock( [], [simple_block] )
#code_expr = PepCode( [], [simple_block] )

@skip
@istest
def standalone_block_can_sit_between_others():

    class MyStandaloneBlock( object ):
        def after( self, next_block ):
            return None  # Don't expect anything
        def unblock( self ):
            return PepPrint( PepInt('3') )
    #assert_implements( MyStandaloneBlock, PepBlock )

    assert_blocked(
        [
            simple_block,
            MyStandaloneBlock(),
            simple_block,
        ],
        [
            simple_block,
            PepPrint( PepInt('3') ),
            simple_block,
        ],
    )


def is_code( block ):
    return True

@skip
@istest
def block_can_suck_following_code():

    class MyCombinedBlock( object ):
        def __init__( self, code ):
            self.code = code
        def after( self, next_block ):
            return None
        def unblock( self ):
            return MyExpr( self.code )

    class MyCodeSuckerBlock( object ):

        def after( self, next_block ):
            if is_code( next_block ):
                return MyCombinedBlock( next_block )
            else:
                raise ExpectedBlock( "code" )

        def unblock( self ):
            # We should never get here
            raise ExpectedBlock( "code" )

    #assert_implements( MyCodeSuckerBlock, PepBlock )

    assert_blocked(
        [
            simple_block,
            MyCodeSuckerBlock(),
            code_block,
            simple_block,
        ],
        [
            simple_block,
            MyCombinedBlock( code_expr ),
            simple_block,
        ],
    )



