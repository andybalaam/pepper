
from cStringIO import StringIO
from nose.tools import *

from parse import LexedLexer

def _lex( string ):
    return list( LexedLexer.Lexer( StringIO( string ) ) )

def _assert_token( token, ( text, tp ) ):
    assert_equal( token.getText(), text )
    assert_equal( token.getType(), tp )

def test_hello_world():
    tokens = _lex( """0001:0008     STRING(Hello, world!)
0001:0024     RPAREN""" )

    _assert_token( tokens[0], ( "0001",            LexedLexer.NUMBER ) )
    _assert_token( tokens[1], ( "0008",            LexedLexer.NUMBER ) )
    _assert_token( tokens[2], ( "STRING",          LexedLexer.SYMBOL ) )
    _assert_token( tokens[3], ( "(Hello, world!)", LexedLexer.CONTENT ) )
    _assert_token( tokens[4], ( "0001",            LexedLexer.NUMBER ) )
    _assert_token( tokens[5], ( "0024",            LexedLexer.NUMBER ) )
    _assert_token( tokens[6], ( "RPAREN",          LexedLexer.SYMBOL ) )

    assert_equal( len( tokens ), 7 )


