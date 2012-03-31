
from cStringIO import StringIO
from nose.tools import *

from tokenutils import Iterable2TokenStream, make_token

from libeeyore.functionvalues import *
from libeeyore.languagevalues import *
from libeeyore.values import *

from parse import EeyoreLexer
from parse import EeyoreParser
from parse import EeyoreTreeWalker
from parse.eeyorestatements import EeyoreStatements

from eeyasserts import assert_multiline_equal

def _parse( tokens ):
    return list( EeyoreStatements( Iterable2TokenStream( tokens ) ) )


def _ast_node_children_to_string( ast, indent ):
    ret = ""
    child = ast.getFirstChild()
    while child is not None:
        ret += _ast_node_to_string( child, indent + 4 )
        child = child.getNextSibling()
    return ret

def _ast_node_to_string( ast, indent ):

    return "{indent}{node}\n{children}".format(
        indent = " " * indent,
        node = "[%s:%s]" % ( EeyoreParser._tokenNames[ast.getType()],
            ast.getText().replace( "\n", "\\n" ) ),
        children = _ast_node_children_to_string( ast, indent ),
        )

def _ast_to_string( ast ):
    return _ast_node_to_string( ast, 0 )

def _parse_to_ast_string( tokens ):
    parser = EeyoreParser.Parser( Iterable2TokenStream( tokens ) )
    parser.program();
    return "\n" + _ast_to_string( parser.getAST() )



double_dedent_tokens = (
    make_token( "def",    EeyoreLexer.LITERAL_def,     1,  1 ),
    make_token( "type",   EeyoreLexer.SYMBOL,          2,  2 ),
    make_token( "myfn",   EeyoreLexer.SYMBOL,          3,  3 ),
    make_token( "(",      EeyoreLexer.LPAREN,          4,  4 ),
    make_token( "int",    EeyoreLexer.SYMBOL,          5,  5 ),
    make_token( "cfg",    EeyoreLexer.SYMBOL,          6,  6 ),
    make_token( ")",      EeyoreLexer.RPAREN,          7,  7 ),
    make_token( ":",      EeyoreLexer.COLON,           8,  8 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,         9,  9 ),
    make_token( "",       EeyoreLexer.INDENT,         10, 10 ),
    make_token( "if",     EeyoreLexer.LITERAL_if,     11, 11 ),
    make_token( "cfg",    EeyoreLexer.SYMBOL,         12, 12 ),
    make_token( ">",      EeyoreLexer.GT,             13, 13 ),
    make_token( "0",      EeyoreLexer.INT,            14, 14 ),
    make_token( ":",      EeyoreLexer.COLON,          15, 15 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        16, 16 ),
    make_token( "",       EeyoreLexer.INDENT,         17, 17 ),
    make_token( "return", EeyoreLexer.LITERAL_return, 18, 18 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         19, 19 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        20, 20 ),
    make_token( "",       EeyoreLexer.DEDENT,         20, 20 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        20, 20 ),
    make_token( "else",   EeyoreLexer.LITERAL_else,   22, 22 ),
    make_token( ":",      EeyoreLexer.COLON,          23, 23 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        24, 24 ),
    make_token( "",       EeyoreLexer.INDENT,         25, 25 ),
    make_token( "return", EeyoreLexer.LITERAL_return, 26, 26 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         27, 27 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        28, 28 ),
    make_token( "",       EeyoreLexer.DEDENT,         28, 28 ),
        # Note:newlines like this are inserted by the post-lex dedent
        # calculation
    make_token( "\n",     EeyoreLexer.NEWLINE,        28, 28 ),
    make_token( "",       EeyoreLexer.DEDENT,         31, 31 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        31, 31 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        32, 32 ),
    )


def test_ast_double_dedent():
    assert_multiline_equal(
        _parse_to_ast_string( double_dedent_tokens ),
        r"""
["def":def]
    [SYMBOL:type]
    [SYMBOL:myfn]
    [LPAREN:(]
        [SYMBOL:int]
        [SYMBOL:cfg]
    [COLON::]
        ["if":if]
            [GT:>]
                [SYMBOL:cfg]
                [INT:0]
            [COLON::]
                ["return":return]
                    [SYMBOL:int]
            ["else":else]
            [COLON::]
                ["return":return]
                    [SYMBOL:int]
"""
        )





calc_type_tokens = (
    make_token( "def",    EeyoreLexer.LITERAL_def,     1,  1 ),
    make_token( "int",    EeyoreLexer.SYMBOL,          2,  2 ),
    make_token( "myfn",   EeyoreLexer.SYMBOL,          3,  3 ),
    make_token( "(",      EeyoreLexer.LPAREN,          4,  4 ),
    make_token( "fn2",    EeyoreLexer.SYMBOL,          5,  5 ),
    make_token( "(",      EeyoreLexer.LPAREN,          6,  6 ),
    make_token( "a",      EeyoreLexer.SYMBOL,          7,  7 ),
    make_token( ",",      EeyoreLexer.COMMA,           8,  8 ),
    make_token( "b",      EeyoreLexer.SYMBOL,          9,  9 ),
    make_token( ")",      EeyoreLexer.RPAREN,         10, 10 ),
    make_token( "cfg",    EeyoreLexer.SYMBOL,         11, 11 ),
    make_token( ")",      EeyoreLexer.RPAREN,         12, 12 ),
    make_token( ":",      EeyoreLexer.COLON,          13, 13 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        14, 14 ),
    make_token( "",       EeyoreLexer.INDENT,         15, 15 ),
    make_token( "pass",   EeyoreLexer.SYMBOL,         16, 16 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        17, 17 ),
    make_token( "",       EeyoreLexer.DEDENT,         18, 18 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        19, 19 ),
    )



def test_ast_calc_type():
    assert_multiline_equal(
        _parse_to_ast_string( calc_type_tokens ),
        r"""
["def":def]
    [SYMBOL:int]
    [SYMBOL:myfn]
    [LPAREN:(]
        [LPAREN:(]
            [SYMBOL:fn2]
            [SYMBOL:a]
            [COMMA:,]
            [SYMBOL:b]
        [SYMBOL:cfg]
    [COLON::]
        [SYMBOL:pass]
"""
        )



def test_calc_type():
    assert_multiline_equal( repr( _parse( calc_type_tokens ) ),
        "[" +
            "EeyDef(" +
                "EeySymbol('int')," +
                "EeySymbol('myfn')," +
                "("+
                    "(" +
                        "EeyFunctionCall(" +
                            "EeySymbol('fn2')," +
                            "(" +
                                "EeySymbol('a'), " +
                                "EeySymbol('b')" +
                            ")" +
                        "), " +
                        "EeySymbol('cfg')" +
                    ")," +
                ")," +
                "(" +
                    "EeySymbol('pass')," +
                ")" +
            ")" +
        "]"
        )




class_keyword_tokens = (
    make_token( "class",   EeyoreLexer.LITERAL_class, 1, 1 ),
    make_token( "MyClass", EeyoreLexer.SYMBOL,        2, 2 ),
    make_token( ":",       EeyoreLexer.COLON,         3, 3 ),
    make_token( "\n",      EeyoreLexer.NEWLINE,       4, 4 ),
    make_token( "",        EeyoreLexer.INDENT,        5, 5 ),
    make_token( "pass",    EeyoreLexer.SYMBOL,        6, 6 ),
    make_token( "\n",      EeyoreLexer.NEWLINE,       7, 7 ),
    make_token( "",        EeyoreLexer.DEDENT,        8, 8 ),
    make_token( "\n",      EeyoreLexer.NEWLINE,       9, 9 ),
    )



def test_ast_class_keyword():
    assert_multiline_equal(
        _parse_to_ast_string( class_keyword_tokens ),
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        [SYMBOL:pass]
"""
        )



def test_class_keyword():
    assert_multiline_equal( repr( _parse( class_keyword_tokens ) ),
        "[" +
            "EeyClass(" +
                "EeySymbol('MyClass')," +
                "()," +
                "(" +
                    "EeySymbol('pass')," +
                ")" +
            ")" +
        "]"
        )




