# Copyright (C) 2012-2014 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

import re
import textwrap

from cStringIO import StringIO

from newsyntaxparse import NewSyntaxPepperParser
import tools_lex

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
        node = "[%s:%s]" % ( NewSyntaxPepperParser._tokenNames[ast.getType()],
            ast.getText().replace( "\n", "\\n" ).replace( "<no text>", "" ) ),
        children = _ast_node_children_to_string( ast, indent ),
        )

def _ast_to_string( ast ):
    return _ast_node_to_string( ast, 0 )

def _ast( lexed ):
    parser = NewSyntaxPepperParser.Parser( lexed )
    parser.program()

    actual_ast = "\n"
    ast = parser.getAST()
    while ast is not None:
        actual_ast += _ast_to_string( ast )
        ast = ast.getNextSibling()

    return actual_ast

def assert_ast( code, expected_ast ):
    assert_multi_line_equal(
        textwrap.dedent( expected_ast ),
        _ast( tools_lex.lex( code ) )
    )

