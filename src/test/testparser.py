
from cStringIO import StringIO
from nose.tools import *

from antlr import CommonToken
from antlr import Token
from antlr import TokenStream

from libeeyore.values import *
from libeeyore.functionvalues import *

from parse import EeyoreLexer
from parse import EeyoreParser
from parse import EeyoreTreeWalker

class Iterable2TokenStream( TokenStream ):
    def __init__( self, lst ):
        self.it = iter( lst )

    def nextToken( self ):
        try:
            return self.it.next()
        except StopIteration:
            return CommonToken( type = Token.EOF_TYPE )

def _parse( tokens ):
    parser = EeyoreParser.Parser( Iterable2TokenStream( tokens ) )
    parser.program();
    walker = EeyoreTreeWalker.Walker()
    return walker.functionCall( parser.getAST() )

def _token( text, tp ):
    ret = CommonToken()
    ret.setText( text )
    ret.setType( tp )
    return ret

def test_hello_world():
    value = _parse( (
        _token( "print",         EeyoreLexer.SYMBOL    ) ,
        _token( "(",             EeyoreLexer.LPAREN    ) ,
        _token( "Hello, world!", EeyoreLexer.STRINGLIT ),
        _token( ")",             EeyoreLexer.RPAREN    ) ,
        ) )

    assert_equal( value.__class__, EeyFunctionCall )
    assert_equal( value.func_name, "print" )

    func = value.func

    assert_equal( func.__class__,   EeySymbol )
    assert_equal( func.symbol_name, "print" )

    args = value.args
    assert_equal( len( args ), 1 )

    assert_equal( args[0].__class__,   EeyString )
    assert_equal( args[0].value, "Hello, world!" )

