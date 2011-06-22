
from cStringIO import StringIO
from nose.tools import *

from parse import EeyoreLexer

def _lex( string ):
    return list( EeyoreLexer.Lexer( StringIO( string ) ) )

def _assert_token( token, ( text, tp ) ):
    assert_equal( token.getText(), text )
    assert_equal( token.getType(), tp )

def test_hello_world():
    tokens = _lex( """print( "Hello, world!" )""" )

    _assert_token( tokens[0], ( "print",         EeyoreLexer.SYMBOL ) )
    _assert_token( tokens[1], ( "(",             EeyoreLexer.LPAREN ) )
    _assert_token( tokens[2], ( "Hello, world!", EeyoreLexer.STRINGLIT ) )
    _assert_token( tokens[3], ( ")",             EeyoreLexer.RPAREN ) )


