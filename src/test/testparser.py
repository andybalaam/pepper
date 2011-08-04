
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

