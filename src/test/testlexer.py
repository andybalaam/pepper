
from cStringIO import StringIO
from nose.tools import *

from parse import EeyoreLexer

def _lex( string ):
    return list( EeyoreLexer.Lexer( StringIO( string ) ) )

def _assert_token( token, text, tp, line = None, col = None ):
    assert_equal( token.getText(), text )
    assert_equal( token.getType(), tp )
    if line is not None:
        assert_equal( token.getLine(), line )
    if col is not None:
        assert_equal( token.getColumn(), col )

def test_hello_world():
    tokens = _lex( """print( "Hello, world!" )""" )

    _assert_token( tokens[0], "print",         EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "(",             EeyoreLexer.LPAREN, 1, 6 )
    _assert_token( tokens[2], "Hello, world!", EeyoreLexer.STRING, 1, 8 )
    _assert_token( tokens[3], ")",             EeyoreLexer.RPAREN, 1, 24 )

    assert_equal( len( tokens ), 4 )

