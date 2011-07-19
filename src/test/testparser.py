
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

def _parse( tokens ):
    return list( EeyoreStatements( Iterable2TokenStream( tokens ) ) )

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
        make_token( "[",     EeyoreLexer.LSQUBR ),
        make_token( "3",     EeyoreLexer.INT ),
        make_token( "]",     EeyoreLexer.RSQUBR ),
        make_token( "\n",    EeyoreLexer.NEWLINE ),
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



