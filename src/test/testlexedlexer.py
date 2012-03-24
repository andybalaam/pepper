
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
0001:0024     RPAREN
""" )

    _assert_token( tokens[ 0], ( "0001",            LexedLexer.NUMBER ) )
    _assert_token( tokens[ 1], ( ":",               LexedLexer.COLON ) )
    _assert_token( tokens[ 2], ( "0008",            LexedLexer.NUMBER ) )
    _assert_token( tokens[ 3], ( "     ",           LexedLexer.SPACES ) )
    _assert_token( tokens[ 4], ( "STRING",          LexedLexer.SYMBOL ) )
    _assert_token( tokens[ 5], ( "(Hello, world!)", LexedLexer.CONTENT ) )
    _assert_token( tokens[ 6], ( "\n",              LexedLexer.NEWLINE ) )
    _assert_token( tokens[ 7], ( "0001",            LexedLexer.NUMBER ) )
    _assert_token( tokens[ 8], ( ":",               LexedLexer.COLON ) )
    _assert_token( tokens[ 9], ( "0024",            LexedLexer.NUMBER ) )
    _assert_token( tokens[10], ( "     ",           LexedLexer.SPACES ) )
    _assert_token( tokens[11], ( "RPAREN",          LexedLexer.SYMBOL ) )
    _assert_token( tokens[12], ( "\n",              LexedLexer.NEWLINE ) )

    assert_equal( len( tokens ), 13 )

def test_quoted():
    tokens = _lex( """0001:0008   "import"(import)
""" )

    _assert_token( tokens[4], ( '"import"', LexedLexer.QUOTED_LITERAL ) )


