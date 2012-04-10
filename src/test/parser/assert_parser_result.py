import re

from cStringIO import StringIO

from parse import EeyoreParser
from parse import EeyoreTreeWalker
from parse.eeyorestatements import EeyoreStatements
from parse.eeyoretokenstreamfromfile import EeyoreTokenStreamFromFile

from test.eeyasserts import assert_multiline_equal

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
            ast.getText().replace( "\n", "\\n" ).replace( "<no text>", "" ) ),
        children = _ast_node_children_to_string( ast, indent ),
        )

def _ast_to_string( ast ):
    return '\n' + _ast_node_to_string( ast, 0 )

# Strip out newlines followed by spaces or a closing bracket
UNPRETTY_RE = re.compile( "\n(\\s+|([)]))" )
def _unprettify( expr ):
    return UNPRETTY_RE.sub( lambda m: m.group(2), expr )

def parse( lexed_input ):
    tokens = EeyoreTokenStreamFromFile( StringIO( lexed_input.lstrip() ) )
    parser = EeyoreParser.Parser( tokens )
    parser.program()
    return parser

def assert_parser_result( lexed_input, expected_ast, expected_parsed ):

    parser = parse( lexed_input )
    actual_ast = _ast_to_string( parser.getAST() )

    assert_multiline_equal( expected_ast, actual_ast )

    tokens = EeyoreTokenStreamFromFile( StringIO( lexed_input.lstrip() ) )
    actual_parsed = "\n".join( repr( s ) for s in EeyoreStatements( tokens ) )
    actual_parsed += "\n"

    # TODO: format actual nicely, instead of expected nastily
    assert_multiline_equal(
        _unprettify( expected_parsed ).strip(),
        actual_parsed.strip() )

