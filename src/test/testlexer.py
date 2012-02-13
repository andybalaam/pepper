
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


def test_import():
    tokens = _lex( """
import a

print()
""" )

    _assert_token( tokens[0], "\n",     EeyoreLexer.NEWLINE,         1, 1 )
    _assert_token( tokens[1], "import", EeyoreLexer.LITERAL_import,  2, 1 )
    _assert_token( tokens[2], "a",      EeyoreLexer.SYMBOL,          2, 8 )
    _assert_token( tokens[3], "\n",     EeyoreLexer.NEWLINE,         2, 9 )
    _assert_token( tokens[4], "\n",     EeyoreLexer.NEWLINE,         3, 1 )
    _assert_token( tokens[5], "print",  EeyoreLexer.SYMBOL,          4, 1 )
    _assert_token( tokens[6], "(",      EeyoreLexer.LPAREN,          4, 6 )
    _assert_token( tokens[7], ")",      EeyoreLexer.RPAREN,          4, 7 )
    _assert_token( tokens[8], "\n",     EeyoreLexer.NEWLINE,         4, 8 )

    assert_equal( len( tokens ), 9 )


def test_qualified_token():
    tokens = _lex( """import sys
print( sys.argv )
""" )

    _assert_token( tokens[0], "import",   EeyoreLexer.LITERAL_import,  1, 1 )
    _assert_token( tokens[1], "sys",      EeyoreLexer.SYMBOL,          1, 8 )
    _assert_token( tokens[2], "\n",       EeyoreLexer.NEWLINE,         1, 11 )
    _assert_token( tokens[3], "print",    EeyoreLexer.SYMBOL,          2, 1 )
    _assert_token( tokens[4], "(",        EeyoreLexer.LPAREN,          2, 6 )
    _assert_token( tokens[5], "sys.argv", EeyoreLexer.SYMBOL,          2, 8 )
    _assert_token( tokens[6], ")",        EeyoreLexer.RPAREN,          2, 17 )
    _assert_token( tokens[7], "\n",       EeyoreLexer.NEWLINE,         2, 18 )

    assert_equal( len( tokens ), 8 )


def test_array_lookup():
    tokens = _lex( """myarr[1]""" )

    _assert_token( tokens[0], "myarr", EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "[",     EeyoreLexer.LSQUBR, 1, 6 )
    _assert_token( tokens[2], "1",     EeyoreLexer.INT,    1, 7 )
    _assert_token( tokens[3], "]",     EeyoreLexer.RSQUBR, 1, 8 )

    assert_equal( len( tokens ), 4 )


def test_operator_plus():
    tokens = _lex( """a + b""" )

    _assert_token( tokens[0], "a", EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "+", EeyoreLexer.PLUS,   1, 3 )
    _assert_token( tokens[2], "b", EeyoreLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )


def test_operator_times():
    tokens = _lex( """a * b""" )

    _assert_token( tokens[0], "a", EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "*", EeyoreLexer.TIMES,  1, 3 )
    _assert_token( tokens[2], "b", EeyoreLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )



def test_operator_gt():
    tokens = _lex( """a > b""" )

    _assert_token( tokens[0], "a", EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], ">", EeyoreLexer.GT,   1, 3 )
    _assert_token( tokens[2], "b", EeyoreLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )


def test_leading_whitespace():
    tokens = _lex( """    a""" )

    _assert_token( tokens[0], "    ", EeyoreLexer.LEADINGSP, 1, 1 )
    _assert_token( tokens[1], "a",    EeyoreLexer.SYMBOL,    1, 5 )
    assert( len( tokens ) == 2 )


def test_double_leading_whitespace():
    tokens = _lex( "a\n        b" )

    _assert_token( tokens[0], "a",        EeyoreLexer.SYMBOL,    1, 1 )
    _assert_token( tokens[1], "\n",       EeyoreLexer.NEWLINE,   1, 2 )
    _assert_token( tokens[2], "        ", EeyoreLexer.LEADINGSP, 2, 1 )
    _assert_token( tokens[3], "b",        EeyoreLexer.SYMBOL,    2, 9 )
    assert( len( tokens ) == 4 )


def test_comment():
    tokens = _lex( """# Comment""" )
    assert( len( tokens ) == 0 )

def test_comment_leading_whitespace():
    tokens = _lex( """    # Comment""" )
    _assert_token( tokens[0], "    ", EeyoreLexer.LEADINGSP, 1, 1 )
    assert( len( tokens ) == 1 )


def test_comment_leading_whitespace_not_multiple_of_4():
    tokens = _lex( """   # Comment""" )
    _assert_token( tokens[0], "   ", EeyoreLexer.LEADINGSP, 1, 1 )
    assert( len( tokens ) == 1 )

def test_simple_initialisation():
    tokens = _lex( "int i = 7" )

    _assert_token( tokens[0], "int", EeyoreLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "i",   EeyoreLexer.SYMBOL, 1, 5 )
    _assert_token( tokens[2], "=",   EeyoreLexer.EQUALS, 1, 7 )
    _assert_token( tokens[3], "7",   EeyoreLexer.INT,    1, 9 )
    assert( len( tokens ) == 4 )

def test_int_literal():
    tokens = _lex( "354" )
    _assert_token( tokens[0], "354", EeyoreLexer.INT )
    assert( len( tokens ) == 1 )

def test_float_literal():
    tokens = _lex( "354.078 65. .45" )
    _assert_token( tokens[0], "354.078", EeyoreLexer.FLOAT )
    _assert_token( tokens[1], "65.",     EeyoreLexer.FLOAT )
    _assert_token( tokens[2], ".45",     EeyoreLexer.FLOAT )
    assert( len( tokens ) == 3 )

