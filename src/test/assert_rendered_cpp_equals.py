# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from cStringIO import StringIO

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

from parse import PepperLexer
from parse.pepperstatements import PepperStatements
from parse.indentdedenttokenstream import IndentDedentTokenStream


def parse_statement( code_input ):
    tokens = IndentDedentTokenStream(
        PepperLexer.Lexer( StringIO( code_input + "\n" ) ) )
    statements = list( PepperStatements( tokens ) )

    assert_equal( 1, len( statements ) )

    return statements[0]


def eval_statement( env, code_input ):
    st = parse_statement( code_input )
    return st.evaluate( env )


def assert_rendered_cpp_equals( expected, code_input ):
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    # make sys available
    eval_statement( env, "import sys" )

    st = parse_statement( code_input )
    actual = st.render( env )

    assert_equal( expected, actual )



