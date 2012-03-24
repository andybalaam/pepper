
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



simple_initialisation_tokens = (
    make_token( "int", EeyoreLexer.SYMBOL,  1, 1 ),
    make_token( "i",   EeyoreLexer.SYMBOL,  1, 5 ),
    make_token( "=",   EeyoreLexer.EQUALS,  1, 7 ),
    make_token( "7",   EeyoreLexer.INT,     1, 9 ),
    make_token( "\n",  EeyoreLexer.NEWLINE, 1, 10 ),
    )

def test_ast_simple_initialisation():
    assert_multiline_equal(
        _parse_to_ast_string( simple_initialisation_tokens ),
        r"""
[EQUALS:=]
    [SYMBOL:int]
    [SYMBOL:i]
    [INT:7]
"""
        )

def test_simple_initialisation():
    assert_multiline_equal( repr( _parse( simple_initialisation_tokens ) ),
        """[EeyInit(EeySymbol('int'),EeySymbol('i'),EeyInt('7'))]"""
        )



float_initialisation_tokens = (
    make_token( "float", EeyoreLexer.SYMBOL,  1, 1 ),
    make_token( "f",     EeyoreLexer.SYMBOL,  1, 7 ),
    make_token( "=",     EeyoreLexer.EQUALS,  1, 9 ),
    make_token( "7.4",   EeyoreLexer.FLOAT,   1, 11 ),
    make_token( "\n",    EeyoreLexer.NEWLINE, 1, 12 ),
    )

def test_ast_simple_initialisation():
    assert_multiline_equal(
        _parse_to_ast_string( float_initialisation_tokens ),
        r"""
[EQUALS:=]
    [SYMBOL:float]
    [SYMBOL:f]
    [FLOAT:7.4]
"""
        )

def test_simple_initialisation():
    assert_multiline_equal( repr( _parse( float_initialisation_tokens ) ),
        """[EeyInit(EeySymbol('float'),EeySymbol('f'),EeyFloat('7.4'))]"""
        )


define_function_noargs_tokens = (
    make_token( "def",    EeyoreLexer.LITERAL_def,    1, 1 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         1, 5 ),
    make_token( "myfn",   EeyoreLexer.SYMBOL,         1, 9 ),
    make_token( "(",      EeyoreLexer.LPAREN,         1, 13 ),
    make_token( ")",      EeyoreLexer.RPAREN,         1, 14 ),
    make_token( ":",      EeyoreLexer.COLON,          1, 15 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        1, 16 ),
    make_token( "",       EeyoreLexer.INDENT,         2, 1 ),
    make_token( "return", EeyoreLexer.LITERAL_return, 2, 4 ),
    make_token( "1",      EeyoreLexer.INT,            2, 11 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 12 ),
    make_token( "",       EeyoreLexer.DEDENT,         2, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 14 ),
    )


def test_ast_define_function_noargs():
    assert_multiline_equal(
        _parse_to_ast_string( define_function_noargs_tokens ),
        r"""
["def":def]
    [SYMBOL:int]
    [SYMBOL:myfn]
    [LPAREN:(]
    [COLON::]
        ["return":return]
            [INT:1]
"""
        )


def test_define_function_noargs():
    assert_multiline_equal( repr( _parse( define_function_noargs_tokens ) ),
        """[EeyDef(EeySymbol('int'),EeySymbol('myfn'),(),(EeyReturn(EeyInt('1')),))]"""
        )


define_function_threeargs_tokens = (
    make_token( "def",    EeyoreLexer.LITERAL_def,    1, 1 ),
    make_token( "void",   EeyoreLexer.SYMBOL,         1, 5 ),
    make_token( "myfn",   EeyoreLexer.SYMBOL,         1, 9 ),
    make_token( "(",      EeyoreLexer.LPAREN,         1, 13 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         1, 15 ),
    make_token( "x",      EeyoreLexer.SYMBOL,         1, 19 ),
    make_token( ",",      EeyoreLexer.COMMA,          1, 20 ),
    make_token( "bool",   EeyoreLexer.SYMBOL,         1, 22 ),
    make_token( "y",      EeyoreLexer.SYMBOL,         1, 27 ),
    make_token( ",",      EeyoreLexer.COMMA,          1, 28 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         1, 30 ),
    make_token( "z",      EeyoreLexer.SYMBOL,         1, 34 ),
    make_token( ")",      EeyoreLexer.RPAREN,         1, 36 ),
    make_token( ":",      EeyoreLexer.COLON,          1, 37 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        1, 38 ),
    make_token( "",       EeyoreLexer.INDENT,         2, 1 ),
    make_token( "pass",   EeyoreLexer.SYMBOL,         2, 4 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 12 ),
    make_token( "",       EeyoreLexer.DEDENT,         2, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 14 ),
    )


def test_ast_define_function_threeargs():
    assert_multiline_equal(
        _parse_to_ast_string( define_function_threeargs_tokens ),
        r"""
["def":def]
    [SYMBOL:void]
    [SYMBOL:myfn]
    [LPAREN:(]
        [SYMBOL:int]
        [SYMBOL:x]
        [COMMA:,]
        [SYMBOL:bool]
        [SYMBOL:y]
        [COMMA:,]
        [SYMBOL:int]
        [SYMBOL:z]
    [COLON::]
        [SYMBOL:pass]
"""
        )


def test_define_function_threeargs():
    assert_multiline_equal( repr( _parse( define_function_threeargs_tokens ) ),
        """[EeyDef(EeySymbol('void'),EeySymbol('myfn'),((EeySymbol('int'), EeySymbol('x')), (EeySymbol('bool'), EeySymbol('y')), (EeySymbol('int'), EeySymbol('z'))),(EeySymbol('pass'),))]"""
        )


call_function_noargs_tokens = (
    make_token( "f",  EeyoreLexer.SYMBOL,  1, 1 ),
    make_token( "(",  EeyoreLexer.LPAREN,  1, 2 ),
    make_token( ")",  EeyoreLexer.RPAREN,  1, 3 ),
    make_token( "\n", EeyoreLexer.NEWLINE, 1, 4 ),
    )

def test_ast_call_function_noargs():
    assert_multiline_equal(
        _parse_to_ast_string( call_function_noargs_tokens ),
        r"""
[LPAREN:(]
    [SYMBOL:f]
"""
        )

def test_call_function_noargs():
    assert_multiline_equal( repr( _parse( call_function_noargs_tokens ) ),
        """[EeyFunctionCall(EeySymbol('f'),())]"""
        )



call_function_threeargs_tokens = (
    make_token( "f",  EeyoreLexer.SYMBOL,  1, 1 ),
    make_token( "(",  EeyoreLexer.LPAREN,  1, 2 ),
    make_token( "1",  EeyoreLexer.INT,     1, 4 ),
    make_token( ",",  EeyoreLexer.COMMA,   1, 5 ),
    make_token( "2",  EeyoreLexer.INT,     1, 7 ),
    make_token( ",",  EeyoreLexer.COMMA,   1, 5 ),
    make_token( "3",  EeyoreLexer.INT,     1, 7 ),
    make_token( ")",  EeyoreLexer.RPAREN,  1, 9 ),
    make_token( "\n", EeyoreLexer.NEWLINE, 1, 10 ),
    )

def test_ast_call_function_threeargs():
    assert_multiline_equal(
        _parse_to_ast_string( call_function_threeargs_tokens ),
        r"""
[LPAREN:(]
    [SYMBOL:f]
    [INT:1]
    [COMMA:,]
    [INT:2]
    [COMMA:,]
    [INT:3]
"""
        )


def test_call_function_threeargs():
    assert_multiline_equal( repr( _parse( call_function_threeargs_tokens ) ),
        """[EeyFunctionCall(EeySymbol('f'),(EeyInt('1'), EeyInt('2'), EeyInt('3')))]"""
        )


define_function_twolines_tokens = (
    make_token( "def",    EeyoreLexer.LITERAL_def,    1, 1 ),
    make_token( "void",   EeyoreLexer.SYMBOL,         1, 5 ),
    make_token( "myfn",   EeyoreLexer.SYMBOL,         1, 9 ),
    make_token( "(",      EeyoreLexer.LPAREN,         1, 13 ),
    make_token( ")",      EeyoreLexer.RPAREN,         1, 36 ),
    make_token( ":",      EeyoreLexer.COLON,          1, 37 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        1, 38 ),
    make_token( "",       EeyoreLexer.INDENT,         2, 1 ),
    make_token( "int",    EeyoreLexer.SYMBOL,         2, 4 ),
    make_token( "a",      EeyoreLexer.SYMBOL,         2, 7 ),
    make_token( "=",      EeyoreLexer.EQUALS,         2, 9 ),
    make_token( "7",      EeyoreLexer.INT,            2, 11 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        2, 12 ),
    make_token( "return", EeyoreLexer.LITERAL_return, 3, 4 ),
    make_token( "a",      EeyoreLexer.SYMBOL,         3, 11 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        3, 12 ),
    make_token( "",       EeyoreLexer.DEDENT,         4, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        3, 12 ),
    make_token( "\n",     EeyoreLexer.NEWLINE,        4, 14 ),
    )


def test_ast_define_function_twolines():
    assert_multiline_equal(
        _parse_to_ast_string( define_function_twolines_tokens ),
        r"""
["def":def]
    [SYMBOL:void]
    [SYMBOL:myfn]
    [LPAREN:(]
    [COLON::]
        [EQUALS:=]
            [SYMBOL:int]
            [SYMBOL:a]
            [INT:7]
        ["return":return]
            [SYMBOL:a]
"""
        )


def test_define_function_twolines():
    assert_multiline_equal( repr( _parse( define_function_twolines_tokens ) ),
        "[EeyDef(" +
            "EeySymbol('void')," +
            "EeySymbol('myfn')," +
            "()," +
            "(" +
                "EeyInit(EeySymbol('int'),EeySymbol('a'),EeyInt('7'))," +
                " EeyReturn(EeySymbol('a'))" +
            "))]"
        )



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




