# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# In the same way, on the outside you appear to people as righteous but on the
# inside you are full of hypocrisy and wickedness.  Matt 23 v28

from nose.tools import *

from assert_parser_result import assert_parser_result_from_code


def test_define_interface_with_one_function():
    assert_parser_result_from_code(
        r"""
interface MyInterface:
    def void foo()
""",
        r"""
["interface":interface]
    [SYMBOL:MyInterface]
    [COLON::]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:foo]
            [LPAREN:(]
""",
        r"""
PepInterface(
    PepSymbol('MyInterface'),
    (),
    (PepInterfaceDef(PepSymbol('void'),PepSymbol('foo'),()),)
)
""" )



def test_comments_in_interface():
    assert_parser_result_from_code(
        r"""
interface MyInterface:
# ignored
    # ignored
    def void foo()
    # ignored
# ignored
""",
        r"""
["interface":interface]
    [SYMBOL:MyInterface]
    [COLON::]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:foo]
            [LPAREN:(]
""",
        r"""
PepInterface(
    PepSymbol('MyInterface'),
    (),
    (PepInterfaceDef(PepSymbol('void'),PepSymbol('foo'),()),)
)
""" )


