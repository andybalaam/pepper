
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




def test_hello_world():
    values = _parse( (
        make_token( "print",         EeyoreLexer.SYMBOL ),
        make_token( "(",             EeyoreLexer.LPAREN ),
        make_token( "Hello, world!", EeyoreLexer.STRING ),
        make_token( ")",             EeyoreLexer.RPAREN ),
        make_token( "\n",            EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyFunctionCall )
    assert_equal( value.func_name, "print" )

    func = value.func

    assert_equal( func.__class__, EeySymbol )
    assert_equal( func.symbol_name, "print" )

    args = value.args
    assert_equal( len( args ), 1 )

    assert_equal( args[0].__class__, EeyString )
    assert_equal( args[0].value, "Hello, world!" )

def test_import():
    values = _parse( (
        make_token( "import", EeyoreLexer.LITERAL_import ),
        make_token( "sys",    EeyoreLexer.SYMBOL ),
        make_token( "\n",     EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyImport )
    assert_equal( value.module_name, "sys" )



def test_multiline():
    values = _parse( (
        make_token( "import",  EeyoreLexer.LITERAL_import ),
        make_token( "sys",     EeyoreLexer.SYMBOL ),
        make_token( "\n",      EeyoreLexer.NEWLINE ),
        make_token( "print",   EeyoreLexer.SYMBOL ),
        make_token( "(",       EeyoreLexer.LPAREN ),
        make_token( "sys.arg", EeyoreLexer.SYMBOL ),
        make_token( ")",       EeyoreLexer.RPAREN ),
        make_token( "\n",      EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 2 )

    assert_equal( values[0].__class__, EeyImport )
    assert_equal( values[1].__class__, EeyFunctionCall )



def test_arraylookup():
    values = _parse( (
        make_token( "myarr", EeyoreLexer.SYMBOL ),
        make_token( "[",     EeyoreLexer.LSQUBR ),
        make_token( "1",     EeyoreLexer.INT ),
        make_token( "]",     EeyoreLexer.RSQUBR ),
        make_token( "\n",    EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyArrayLookup )

    array_value = value.array_value
    assert_equal( array_value.__class__, EeySymbol )
    assert_equal( array_value.symbol_name, "myarr" )

    index = value.index
    assert_equal( index.__class__, EeyInt )
    assert_equal( index.value, "1" )



def test_function_with_arraylookup():
    values = _parse( (
        make_token( "print", EeyoreLexer.SYMBOL ),
        make_token( "(",     EeyoreLexer.LPAREN ),
        make_token( "myarr", EeyoreLexer.SYMBOL ),
        make_token( "[",     EeyoreLexer.LSQUBR ),
        make_token( "2",     EeyoreLexer.INT ),
        make_token( "]",     EeyoreLexer.RSQUBR ),
        make_token( ")",     EeyoreLexer.RPAREN ),
        make_token( "\n",    EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyFunctionCall )

    func = value.func
    assert_equal( func.__class__, EeySymbol )
    assert_equal( func.symbol_name, "print" )

    args = value.args
    assert_equal( len( args ), 1 )

    arrlkp = args[0]
    assert_equal( arrlkp.__class__, EeyArrayLookup )

    array_value = arrlkp.array_value
    assert_equal( array_value.__class__, EeySymbol )
    assert_equal( array_value.symbol_name, "myarr" )

    index = arrlkp.index
    assert_equal( index.__class__, EeyInt )
    assert_equal( index.value, "2" )



def test_arraylookup_qualified():
    values = _parse( (
        make_token( "a.b", EeyoreLexer.SYMBOL ),
        make_token( "[",   EeyoreLexer.LSQUBR ),
        make_token( "3",   EeyoreLexer.INT ),
        make_token( "]",   EeyoreLexer.RSQUBR ),
        make_token( "\n",  EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyArrayLookup )

    array_value = value.array_value
    assert_equal( array_value.__class__, EeySymbol )
    assert_equal( array_value.symbol_name, "a.b" )

    index = value.index
    assert_equal( index.__class__, EeyInt )
    assert_equal( index.value, "3" )



def test_operator_plus():
    values = _parse( (
        make_token( "a", EeyoreLexer.SYMBOL ),
        make_token( "+", EeyoreLexer.PLUS ),
        make_token( "b", EeyoreLexer.SYMBOL ),
        make_token( "\n", EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyPlus )

    assert_equal( value.left_value.__class__, EeySymbol )
    assert_equal( value.left_value.symbol_name, "a" )

    assert_equal( value.right_value.__class__, EeySymbol )
    assert_equal( value.right_value.symbol_name, "b" )


operator_gt_tokens = (
    make_token( "a", EeyoreLexer.SYMBOL ),
    make_token( ">", EeyoreLexer.GT ),
    make_token( "b", EeyoreLexer.SYMBOL ),
    make_token( "\n", EeyoreLexer.NEWLINE ),
    )

def test_ast_operator_gt():
    assert_multiline_equal(
        _parse_to_ast_string( operator_gt_tokens ),
        r"""
[GT:>]
    [SYMBOL:a]
    [SYMBOL:b]
"""
        )


def test_operator_gt():
    assert_multiline_equal( repr( _parse( operator_gt_tokens ) ),
        """[EeyGreaterThan(EeySymbol('a'),EeySymbol('b'))]"""
        )



def test_plus_in_function_call():
    values = _parse( (
        make_token( "print", EeyoreLexer.SYMBOL ),
        make_token( "(",     EeyoreLexer.LPAREN ),
        make_token( "3",     EeyoreLexer.INT ),
        make_token( "+",     EeyoreLexer.PLUS ),
        make_token( "b",     EeyoreLexer.SYMBOL ),
        make_token( ")",     EeyoreLexer.RPAREN ),
        make_token( "\n",    EeyoreLexer.NEWLINE ),
        ) )

    assert_equal( len( values ), 1 )
    value = values[0]

    assert_equal( value.__class__, EeyFunctionCall )

    func = value.func
    assert_equal( func.__class__, EeySymbol )
    assert_equal( func.symbol_name, "print" )

    args = value.args
    assert_equal( len( args ), 1 )

    plus = args[0]
    assert_equal( plus.__class__, EeyPlus )

    assert_equal( plus.left_value.__class__, EeyInt )
    assert_equal( plus.left_value.value, "3" )

    assert_equal( plus.right_value.__class__, EeySymbol )
    assert_equal( plus.right_value.symbol_name, "b" )


single_statement_if_tokens = (
    make_token( "if",    EeyoreLexer.LITERAL_if, 1, 1 ),
    make_token( "True",  EeyoreLexer.SYMBOL,     1, 4 ),
    make_token( ":",     EeyoreLexer.COLON,      1, 8 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    1, 9 ),
    make_token( "",      EeyoreLexer.INDENT,     2, 1 ),
    make_token( "print", EeyoreLexer.SYMBOL,     2, 5 ),
    make_token( "(",     EeyoreLexer.LPAREN,     2, 11 ),
    make_token( "3",     EeyoreLexer.INT,        2, 13 ),
    make_token( ")",     EeyoreLexer.RPAREN,     2, 15 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    2, 16 ),
    make_token( "",      EeyoreLexer.DEDENT,     2, 16 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    3, 1 ),
    )

def test_ast_single_statement_if():
    assert_multiline_equal(
        _parse_to_ast_string( single_statement_if_tokens ),
        r"""
["if":if]
    [SYMBOL:True]
    [COLON::]
    [INDENT:]
        [NEWLINE:\n]
        [LPAREN:(]
            [SYMBOL:print]
            [INT:3]
        [NEWLINE:\n]
        [DEDENT:]
"""
        )


def test_single_statement_if():
    assert_multiline_equal( repr( _parse( single_statement_if_tokens ) ),
        """[EeyIf(EeySymbol('True'),(EeyFunctionCall(EeySymbol('print'),(EeyInt('3'),)),))]"""
        )


def test_if_function_call():
    assert_multiline_equal( repr( _parse( (
        make_token( "if",    EeyoreLexer.LITERAL_if, 1, 1 ),
        make_token( "f",     EeyoreLexer.SYMBOL,     1, 4 ),
        make_token( "(",     EeyoreLexer.LPAREN,     1, 5 ),
        make_token( "3",     EeyoreLexer.INT,        1, 7 ),
        make_token( ")",     EeyoreLexer.RPAREN,     1, 9 ),
        make_token( ":",     EeyoreLexer.COLON,      1, 10 ),
        make_token( "\n",    EeyoreLexer.NEWLINE,    1, 11 ),
        make_token( "",      EeyoreLexer.INDENT,     2, 1 ),
        make_token( "3",     EeyoreLexer.INT,        2, 5 ),
        make_token( "\n",    EeyoreLexer.NEWLINE,    2, 6 ),
        make_token( "",      EeyoreLexer.DEDENT,     2, 6 ),
        make_token( "\n",    EeyoreLexer.NEWLINE,    3, 1 ),
        ) ) ),
        """[EeyIf(EeyFunctionCall(EeySymbol('f'),(EeyInt('3'),)),(EeyInt('3'),))]"""
        )



if_operator_tokens = (
    make_token( "if",    EeyoreLexer.LITERAL_if, 1, 1 ),
    make_token( "3",     EeyoreLexer.INT,        1, 4 ),
    make_token( ">",     EeyoreLexer.GT,         1, 6 ),
    make_token( "4",     EeyoreLexer.INT,        1, 8 ),
    make_token( ":",     EeyoreLexer.COLON,      1, 9 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    1, 10 ),
    make_token( "",      EeyoreLexer.INDENT,     2, 1 ),
    make_token( "3",     EeyoreLexer.INT,        2, 5 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    2, 6 ),
    make_token( "",      EeyoreLexer.DEDENT,     2, 6 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    3, 1 ),
    )

def test_ast_if_operator():

    assert_multiline_equal(
        _parse_to_ast_string( if_operator_tokens ),
        r"""
["if":if]
    [GT:>]
        [INT:3]
        [INT:4]
    [COLON::]
    [INDENT:]
        [NEWLINE:\n]
        [INT:3]
        [NEWLINE:\n]
        [DEDENT:]
"""
        )

def test_if_operator():
    assert_multiline_equal( repr( _parse( if_operator_tokens ) ),
        """[EeyIf(EeyGreaterThan(EeyInt('3'),EeyInt('4')),(EeyInt('3'),))]"""
        )



if_op_fn_tokens = (
    make_token( "if",    EeyoreLexer.LITERAL_if, 1, 1 ),
    make_token( "f",     EeyoreLexer.SYMBOL,     1, 4 ),
    make_token( "(",     EeyoreLexer.LPAREN,     1, 5 ),
    make_token( "a",     EeyoreLexer.SYMBOL,     1, 7 ),
    make_token( ")",     EeyoreLexer.RPAREN,     1, 9 ),
    make_token( ">",     EeyoreLexer.GT,         1, 11 ),
    make_token( "4",     EeyoreLexer.INT,        1, 13 ),
    make_token( ":",     EeyoreLexer.COLON,      1, 14 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    1, 15 ),
    make_token( "",      EeyoreLexer.INDENT,     2, 1 ),
    make_token( "3",     EeyoreLexer.INT,        2, 5 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    2, 6 ),
    make_token( "",      EeyoreLexer.DEDENT,     2, 6 ),
    make_token( "\n",    EeyoreLexer.NEWLINE,    3, 1 ),
    )


def test_ast_if_op_fn():

    assert_multiline_equal(
        _parse_to_ast_string( if_op_fn_tokens ),
        r"""
["if":if]
    [GT:>]
        [LPAREN:(]
            [SYMBOL:f]
            [SYMBOL:a]
        [INT:4]
    [COLON::]
    [INDENT:]
        [NEWLINE:\n]
        [INT:3]
        [NEWLINE:\n]
        [DEDENT:]
"""
        )



def test_if_op_fn():
    assert_multiline_equal( repr( _parse( if_op_fn_tokens ) ),
        """[EeyIf(EeyGreaterThan(EeyFunctionCall(EeySymbol('f'),(EeySymbol('a'),)),EeyInt('4')),(EeyInt('3'),))]"""
        )


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
    make_token( "",       EeyoreLexer.DEDENT,         2, 13 ),
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
    [INDENT:]
        [NEWLINE:\n]
        ["return":return]
            [INT:1]
        [NEWLINE:\n]
        [DEDENT:]
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
    make_token( "",       EeyoreLexer.DEDENT,         2, 13 ),
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
    [INDENT:]
        [NEWLINE:\n]
        [SYMBOL:pass]
        [NEWLINE:\n]
        [DEDENT:]
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
    make_token( "",       EeyoreLexer.DEDENT,         4, 13 ),
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
    [INDENT:]
        [NEWLINE:\n]
        [EQUALS:=]
            [SYMBOL:int]
            [SYMBOL:a]
            [INT:7]
        [NEWLINE:\n]
        ["return":return]
            [SYMBOL:a]
        [NEWLINE:\n]
        [DEDENT:]
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


