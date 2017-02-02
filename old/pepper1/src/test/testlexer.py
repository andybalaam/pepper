# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from cStringIO import StringIO
from nose.tools import *

from parse import PepperLexer

def _lex( string ):
    return list( PepperLexer.Lexer( StringIO( string ) ) )

def _assert_token( token, text, tp, line = None, col = None ):
    assert_equal( token.getText(), text )
    assert_equal( token.getType(), tp )
    if line is not None:
        assert_equal( token.getLine(), line )
    if col is not None:
        assert_equal( token.getColumn(), col )

def test_hello_world():
    tokens = _lex( """print( "Hello, world!" )""" )

    _assert_token( tokens[0], "print",         PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "(",             PepperLexer.LPAREN, 1, 6 )
    _assert_token( tokens[2], "Hello, world!", PepperLexer.STRING, 1, 8 )
    _assert_token( tokens[3], ")",             PepperLexer.RPAREN, 1, 24 )

    assert_equal( len( tokens ), 4 )


def test_import():
    tokens = _lex( """
import a

print()
""" )

    _assert_token( tokens[0], "\n",     PepperLexer.NEWLINE,         1, 1 )
    _assert_token( tokens[1], "import", PepperLexer.LITERAL_import,  2, 1 )
    _assert_token( tokens[2], "a",      PepperLexer.SYMBOL,          2, 8 )
    _assert_token( tokens[3], "\n",     PepperLexer.NEWLINE,         2, 9 )
    _assert_token( tokens[4], "\n",     PepperLexer.NEWLINE,         3, 1 )
    _assert_token( tokens[5], "print",  PepperLexer.SYMBOL,          4, 1 )
    _assert_token( tokens[6], "(",      PepperLexer.LPAREN,          4, 6 )
    _assert_token( tokens[7], ")",      PepperLexer.RPAREN,          4, 7 )
    _assert_token( tokens[8], "\n",     PepperLexer.NEWLINE,         4, 8 )

    assert_equal( len( tokens ), 9 )


def test_qualified_token():
    tokens = _lex( """import sys
print( sys.argv )
""" )

    _assert_token( tokens[0], "import",   PepperLexer.LITERAL_import,  1, 1 )
    _assert_token( tokens[1], "sys",      PepperLexer.SYMBOL,          1, 8 )
    _assert_token( tokens[2], "\n",       PepperLexer.NEWLINE,         1, 11 )
    _assert_token( tokens[3], "print",    PepperLexer.SYMBOL,          2, 1 )
    _assert_token( tokens[4], "(",        PepperLexer.LPAREN,          2, 6 )
    _assert_token( tokens[5], "sys.argv", PepperLexer.SYMBOL,          2, 8 )
    _assert_token( tokens[6], ")",        PepperLexer.RPAREN,          2, 17 )
    _assert_token( tokens[7], "\n",       PepperLexer.NEWLINE,         2, 18 )

    assert_equal( len( tokens ), 8 )


def test_array_lookup():
    tokens = _lex( """myarr[1]""" )

    _assert_token( tokens[0], "myarr", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "[",     PepperLexer.LSQUBR, 1, 6 )
    _assert_token( tokens[2], "1",     PepperLexer.INT,    1, 7 )
    _assert_token( tokens[3], "]",     PepperLexer.RSQUBR, 1, 8 )

    assert_equal( len( tokens ), 4 )


def test_operator_plus():
    tokens = _lex( """a + b""" )

    _assert_token( tokens[0], "a", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "+", PepperLexer.PLUS,   1, 3 )
    _assert_token( tokens[2], "b", PepperLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )


def test_operator_times():
    tokens = _lex( """a * b""" )

    _assert_token( tokens[0], "a", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "*", PepperLexer.TIMES,  1, 3 )
    _assert_token( tokens[2], "b", PepperLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )



def test_operator_gt():
    tokens = _lex( """a > b""" )

    _assert_token( tokens[0], "a", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], ">", PepperLexer.GT,     1, 3 )
    _assert_token( tokens[2], "b", PepperLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )

def test_operator_lt():
    tokens = _lex( """a < b""" )

    _assert_token( tokens[0], "a", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "<", PepperLexer.LT,     1, 3 )
    _assert_token( tokens[2], "b", PepperLexer.SYMBOL, 1, 5 )

    assert_equal( len( tokens ), 3 )


def test_leading_whitespace():
    tokens = _lex( """    a""" )

    _assert_token( tokens[0], "    ", PepperLexer.LEADINGSP, 1, 1 )
    _assert_token( tokens[1], "a",    PepperLexer.SYMBOL,    1, 5 )
    assert( len( tokens ) == 2 )


def test_double_leading_whitespace():
    tokens = _lex( "a\n        b" )

    _assert_token( tokens[0], "a",        PepperLexer.SYMBOL,    1, 1 )
    _assert_token( tokens[1], "\n",       PepperLexer.NEWLINE,   1, 2 )
    _assert_token( tokens[2], "        ", PepperLexer.LEADINGSP, 2, 1 )
    _assert_token( tokens[3], "b",        PepperLexer.SYMBOL,    2, 9 )
    assert( len( tokens ) == 4 )


def test_comment():
    tokens = _lex( """# Comment""" )
    assert( len( tokens ) == 0 )

def test_comment_leading_whitespace():
    tokens = _lex( """    # Comment""" )
    _assert_token( tokens[0], "    ", PepperLexer.LEADINGSP, 1, 1 )
    assert( len( tokens ) == 1 )


def test_comment_leading_whitespace_not_multiple_of_4():
    tokens = _lex( """   # Comment""" )
    _assert_token( tokens[0], "   ", PepperLexer.LEADINGSP, 1, 1 )
    assert( len( tokens ) == 1 )

def test_simple_initialisation():
    tokens = _lex( "int i = 7" )

    _assert_token( tokens[0], "int", PepperLexer.SYMBOL, 1, 1 )
    _assert_token( tokens[1], "i",   PepperLexer.SYMBOL, 1, 5 )
    _assert_token( tokens[2], "=",   PepperLexer.EQUALS, 1, 7 )
    _assert_token( tokens[3], "7",   PepperLexer.INT,    1, 9 )
    assert( len( tokens ) == 4 )

def test_int_literal():
    tokens = _lex( "354" )
    _assert_token( tokens[0], "354", PepperLexer.INT )
    assert( len( tokens ) == 1 )

def test_float_literal():
    tokens = _lex( "354.078 65. .45" )
    _assert_token( tokens[0], "354.078", PepperLexer.FLOAT )
    _assert_token( tokens[1], "65.",     PepperLexer.FLOAT )
    _assert_token( tokens[2], ".45",     PepperLexer.FLOAT )
    assert( len( tokens ) == 3 )


def test_triple_quote():
    tokens = _lex( '""" foo bar """' )
    _assert_token( tokens[0], " foo bar ", PepperLexer.STRING )
    assert( len( tokens ) == 1 )



def test_2_triple_quotes():
    tokens = _lex( '""" foo bar """ """baz quux"""' )
    _assert_token( tokens[0], " foo bar ", PepperLexer.STRING )
    _assert_token( tokens[1], "baz quux",  PepperLexer.STRING )
    assert( len( tokens ) == 2 )




