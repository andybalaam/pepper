
from cStringIO import StringIO
from nose.tools import *

from tokenutils import Iterable2TokenStream, make_token

from libeeyore.values import *
from libeeyore.functionvalues import *

from parse import EeyoreLexer
from parse import EeyoreParser
from parse import EeyoreTreeWalker

def _parse( tokens ):
    parser = EeyoreParser.Parser( Iterable2TokenStream( tokens ) )
    parser.program();
    walker = EeyoreTreeWalker.Walker()
    return walker.functionCall( parser.getAST() )

def test_hello_world():
    value = _parse( (
        make_token( "print",         EeyoreLexer.SYMBOL ),
        make_token( "(",             EeyoreLexer.LPAREN ),
        make_token( "Hello, world!", EeyoreLexer.STRING ),
        make_token( ")",             EeyoreLexer.RPAREN ),
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

