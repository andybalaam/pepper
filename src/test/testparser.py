
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




