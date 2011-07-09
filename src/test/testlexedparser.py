
from cStringIO import StringIO
from nose.tools import *

from tokenutils import Iterable2TokenStream, make_token

from parse import EeyoreLexer
from parse import LexedLexer
from parse import LexedParser

def _parse( tokens ):
    parser = LexedParser.Parser( Iterable2TokenStream( tokens ) )
    return parser.program();

def test_2_lines():
    value = _parse( (
        make_token( "0002",            LexedLexer.NUMBER ),
        make_token( ":",               LexedLexer.COLON ),
        make_token( "0008",            LexedLexer.NUMBER ),
        make_token( "  ",              LexedLexer.SPACES ),
        make_token( "STRING",          LexedLexer.SYMBOL ),
        make_token( "(Hello, world!)", LexedLexer.CONTENT ),
        make_token( "\n",              LexedLexer.NEWLINE ),
        make_token( "0003",            LexedLexer.NUMBER ),
        make_token( ":",               LexedLexer.COLON ),
        make_token( "0001",            LexedLexer.NUMBER ),
        make_token( "  ",              LexedLexer.SPACES ),
        make_token( "RPAREN",          LexedLexer.SYMBOL ),
        make_token( "\n",              LexedLexer.NEWLINE ),
        ) )

    assert_equal( value[0].getText(),   "Hello, world!" )
    assert_equal( value[0].getType(),   EeyoreLexer.STRING )
    assert_equal( value[0].getLine(),   2 )
    assert_equal( value[0].getColumn(), 8 )

    assert_equal( value[1].getType(),   EeyoreLexer.RPAREN )
    assert_equal( value[1].getLine(),   3 )
    assert_equal( value[1].getColumn(), 1 )

    assert_equal( len( value ), 2 )


