# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from cStringIO import StringIO
from nose.tools import *

from tokenutils import Iterable2TokenStream, make_token

from parse import EeyoreLexer
from parse import LexedLexer
from parse import LexedParser

def _parse( tokens ):
    return LexedParser.Parser( Iterable2TokenStream( tokens ) )

def test_2_lines():
    value = _parse( (
        make_token( "0002",          LexedLexer.NUMBER ),
        make_token( ":",             LexedLexer.COLON ),
        make_token( "0008",          LexedLexer.NUMBER ),
        make_token( "  ",            LexedLexer.SPACES ),
        make_token( "STRING",        LexedLexer.SYMBOL ),
        make_token( "Hello, world!", LexedLexer.CONTENT ),
        make_token( "0003",          LexedLexer.NUMBER ),
        make_token( ":",             LexedLexer.COLON ),
        make_token( "0001",          LexedLexer.NUMBER ),
        make_token( "  ",            LexedLexer.SPACES ),
        make_token( "RPAREN",        LexedLexer.SYMBOL ),
        make_token( "\n",            LexedLexer.NEWLINE ),
        ) )

    val = value.line()
    assert_equal( val.getText(),   "Hello, world!" )
    assert_equal( val.getType(),   EeyoreLexer.STRING )
    assert_equal( val.getLine(),   2 )
    assert_equal( val.getColumn(), 8 )

    val = value.line()
    assert_equal( val.getType(),   EeyoreLexer.RPAREN )
    assert_equal( val.getLine(),   3 )
    assert_equal( val.getColumn(), 1 )

    val = value.line()
    assert( val is None )


