
from cStringIO import StringIO
from nose.tools import *

from parse import EeyoreLexer
from parse.indentdedenttokensource import IndentDedentTokenSource
from parse.eeyoretokenstreamfromfile import EeyoreTokenStreamFromFile
from parse.eeyoretokentostring import render_token
from tokenutils import Iterable2TokenStream, make_token

def _tokens_2_string( tokens ):
    return "\n" + "\n".join( render_token( token ) for token in tokens ) + "\n"

def _assert_indent_dedent_generated( before, after ):
    assert_equal(
        _tokens_2_string(
            IndentDedentTokenSource( EeyoreTokenStreamFromFile(
                StringIO( before.lstrip() ) ) ) ),
        after
        )

def test_no_indent():
    _assert_indent_dedent_generated(
        """
0001:0001     SYMBOL(print)
0001:0006     LPAREN
0001:0008     STRING(Hello, world!)
0001:0024     RPAREN
0001:0025    NEWLINE
""",
        """
0001:0001     SYMBOL(print)
0001:0006     LPAREN
0001:0008     STRING(Hello, world!)
0001:0024     RPAREN
0001:0025    NEWLINE
"""
        )

