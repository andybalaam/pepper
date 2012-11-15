# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

import re

from cStringIO import StringIO

from parse import PepperLexer
from parse import PepperParser
from parse import PepperTreeWalker
from parse.pepperstatements import PepperStatements
from parse.peppertokenstreamfromfile import PepperTokenStreamFromFile
from parse.indentdedenttokenstream import IndentDedentTokenStream
from parse.iterablefromtokenstream import IterableFromTokenStream

from test.tokenutils import Iterable2TokenStream

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
        node = "[%s:%s]" % ( PepperParser._tokenNames[ast.getType()],
            ast.getText().replace( "\n", "\\n" ).replace( "<no text>", "" ) ),
        children = _ast_node_children_to_string( ast, indent ),
        )

def _ast_to_string( ast ):
    return '\n' + _ast_node_to_string( ast, 0 )

# Strip out newlines followed by spaces or a closing bracket
UNPRETTY_RE = re.compile( "\n(\\s+|([)]))" )
def _unprettify( expr ):
    return UNPRETTY_RE.sub( lambda m: m.group(2), expr )


def _assert_parser_result_from_token_stream(
    token_stream, expected_ast, expected_parsed
):
    tokens_list = [token for token in token_stream]

    tokens = Iterable2TokenStream( tokens_list )
    parser = PepperParser.Parser( tokens )
    parser.program()

    actual_ast = _ast_to_string( parser.getAST() )

    assert_multiline_equal( expected_ast, actual_ast )

    tokens = Iterable2TokenStream( tokens_list )
    actual_parsed = "\n".join( repr( s ) for s in PepperStatements( tokens ) )
    actual_parsed += "\n"

    # TODO: format actual nicely, instead of expected nastily
    assert_multiline_equal(
        _unprettify( expected_parsed ).strip(),
        actual_parsed.strip() )

def parse_string( lexed_input ):
    tokens = PepperTokenStreamFromFile( StringIO( lexed_input.lstrip() ) )
    parser = PepperParser.Parser( tokens )
    parser.program()
    return parser

def assert_parser_result( lexed_input, expected_ast, expected_parsed ):
    tokens = PepperTokenStreamFromFile( StringIO( lexed_input.lstrip() ) )

    _assert_parser_result_from_token_stream(
        tokens, expected_ast, expected_parsed )

def assert_parser_result_from_code( code_input, expected_ast, expected_parsed ):
    tokens = IndentDedentTokenStream(
        PepperLexer.Lexer( StringIO( code_input ) ) )

    _assert_parser_result_from_token_stream(
        tokens, expected_ast, expected_parsed )

