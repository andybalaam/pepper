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

from pepasserts import assert_multiline_equal

def parse_program( code_input ):
    tokens = IndentDedentTokenStream(
        PepperLexer.Lexer( StringIO( code_input + "\n" ) ) )
    return list( PepperStatements( tokens ) )


def parse_statement( code_input ):
    statements = parse_program( code_input )
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

def assert_rendered_program_equals( expected, code_input ):
    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )
    statements = parse_program( code_input )
    actual = env.render_exe( statements )
    assert_multiline_equal( expected, actual )


