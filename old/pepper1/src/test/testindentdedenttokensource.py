# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from cStringIO import StringIO
from nose.tools import *

from libpepper.usererrorexception import PepUserErrorException
from parse.indentdedenttokenstream import IndentDedentTokenStream
from parse.peppertokenstreamfromfile import PepperTokenStreamFromFile
from parse.peppertokentostring import render_token

from pepasserts import assert_multiline_equal

def _tokens_2_string( tokens ):
    return "\n" + "\n".join( render_token( token ) for token in tokens ) + "\n"

def _indent_dedent_token_string( before ):
    return IndentDedentTokenStream( PepperTokenStreamFromFile(
        StringIO( before.lstrip() ) ) )

def _assert_indent_dedent_generated( before, after ):
    assert_multiline_equal(
        _tokens_2_string( _indent_dedent_token_string( before ) ),
        after )

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

def test_strip_comment_lines():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0025    NEWLINE
0002:0001     SYMBOL(a)
0002:0002    NEWLINE
""",
        """
0001:0025    NEWLINE
0002:0001     SYMBOL(a)
0002:0002    NEWLINE
"""
        )

def test_strip_comment_lines_not_divisible_by_4():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(   )
0001:0025    NEWLINE
0002:0001     SYMBOL(a)
0002:0002    NEWLINE
""",
        """
0001:0025    NEWLINE
0002:0001     SYMBOL(a)
0002:0002    NEWLINE
"""
        )



def test_indent_single_line():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0001:0006     DEDENT
0001:0006    NEWLINE
"""
        )

@raises( PepUserErrorException )
def test_indent_not_divisible_by_4():
    for x in _indent_dedent_token_string(
        """
0001:0001  LEADINGSP(   )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
"""
            ):
        pass


def test_indent_multiline_block():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001  LEADINGSP(    )
0002:0005     SYMBOL(b)
0002:0006    NEWLINE
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0005     SYMBOL(b)
0002:0006    NEWLINE
0002:0006     DEDENT
0002:0006    NEWLINE
"""
        )


def test_multiple_layers_of_indent():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001  LEADINGSP(        )
0002:0009     SYMBOL(b)
0002:0010    NEWLINE
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001     INDENT
0002:0009     SYMBOL(b)
0002:0010    NEWLINE
0002:0010     DEDENT
0002:0010    NEWLINE
0002:0010     DEDENT
0002:0010    NEWLINE
"""
        )




def test_dedent_at_end_even_when_last_line_has_leading_space():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001  LEADINGSP(    )
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0001:0006     DEDENT
0001:0006    NEWLINE
"""
        )



def test_no_dedent_in_middle_of_block():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001    NEWLINE
0003:0001  LEADINGSP(    )
0003:0005     SYMBOL(b)
0003:0006    NEWLINE
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001    NEWLINE
0003:0005     SYMBOL(b)
0003:0006    NEWLINE
0003:0006     DEDENT
0003:0006    NEWLINE
"""
        )




def test_dedent_at_end_even_when_last_line_has_no_newline():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0000:0000     DEDENT
0000:0000    NEWLINE
"""
        )
    # Line and column are messed up because there is no newline at end.


def test_indent_and_dedent_before_end():
    _assert_indent_dedent_generated(
        """
0001:0001  LEADINGSP(    )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001  LEADINGSP(        )
0002:0009     SYMBOL(b)
0002:0010    NEWLINE
0003:0001  LEADINGSP(    )
0003:0005     SYMBOL(c)
0003:0006    NEWLINE
0004:0001     SYMBOL(d)
0004:0002    NEWLINE
""",
        """
0001:0001     INDENT
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001     INDENT
0002:0009     SYMBOL(b)
0002:0010    NEWLINE
0002:0010     DEDENT
0002:0010    NEWLINE
0003:0005     SYMBOL(c)
0003:0006    NEWLINE
0003:0006     DEDENT
0003:0006    NEWLINE
0004:0001     SYMBOL(d)
0004:0002    NEWLINE
"""
        )



@raises( PepUserErrorException )
def test_dedent_to_unknown_indentation():
    for x in _indent_dedent_token_string(
        """
0001:0001  LEADINGSP(        )
0001:0005     SYMBOL(a)
0001:0006    NEWLINE
0002:0001  LEADINGSP(    )
0002:0009     SYMBOL(b)
0002:0010    NEWLINE
"""
            ):
        pass


