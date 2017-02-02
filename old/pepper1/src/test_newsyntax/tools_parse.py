# Copyright (C) 2012-2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

import re
import textwrap
from cStringIO import StringIO

from newsyntaxparse import NewSyntaxPepperParser
from newsyntaxparse.newsyntaxpepperstatements import NewSyntaxPepperStatements

import tools_lex

# Strip out newlines followed by spaces or a closing bracket
UNPRETTY_RE = re.compile( "\n(\\s+|([)]))" )
def _unprettify( expr ):
    return UNPRETTY_RE.sub( lambda m: m.group(2), expr ).strip()

def _parse( lexed ):
    return (
        "\n".join(
            repr( s ) for s in NewSyntaxPepperStatements( lexed ) )
        )

def assert_parsed( code, expected_parsed ):
    assert_multi_line_equal(
        _unprettify( textwrap.dedent( expected_parsed ) ),
        _parse( tools_lex.lex( code ) )
    )

