# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from assert_parser_result import assert_parser_result
from assert_parser_result import assert_parser_result_from_code
from assert_parser_result import parse_string

import antlr

def test_empty_class():
    assert_parser_result(
        r"""
0001:0001    "class"(class)
0001:0007     SYMBOL(MyClass)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(pass)
0002:0009    NEWLINE
0002:0009     DEDENT
0002:0009    NEWLINE
0003:0001    NEWLINE
0004:0001    NEWLINE
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        [SYMBOL:pass]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepSymbol('pass'),
    )
)
""" )


def test_static_member_variable():
    assert_parser_result(
        r"""
0001:0001    "class"(class)
0001:0007     SYMBOL(MyClass)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(int)
0002:0009     SYMBOL(x)
0002:0011     EQUALS(=)
0002:0013        INT(3)
0002:0014    NEWLINE
0002:0014     DEDENT
0002:0014    NEWLINE
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        [EQUALS:=]
            [SYMBOL:int]
            [SYMBOL:x]
            [INT:3]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepInit(
            PepSymbol('int'),
            PepSymbol('x'),
            PepInt('3')
        ),
    )
)
""" )




def test_method():
    assert_parser_result(
        r"""
0001:0001    "class"(class)
0001:0007     SYMBOL(MyClass)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005      "def"(def)
0002:0009     SYMBOL(void)
0002:0014     SYMBOL(myfn)
0002:0018     LPAREN
0002:0019     RPAREN
0002:0020      COLON(:)
0002:0021    NEWLINE
0003:0001     INDENT
0003:0009     SYMBOL(pass)
0003:0013    NEWLINE
0003:0013     DEDENT
0003:0013    NEWLINE
0003:0013     DEDENT
0003:0013    NEWLINE
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:myfn]
            [LPAREN:]
            [COLON::]
                [SYMBOL:pass]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDef(
            PepSymbol('void'),
            PepSymbol('myfn'),
            (),
            (
                PepSymbol('pass'),
            )
        ),
    )
)
""" )



@raises( antlr.MismatchedTokenException )
def test_def_init_outside_class_is_an_error():
    parse_string( r"""
0001:0001 "def_init"(def_init)
0001:0010     LPAREN
0001:0012     SYMBOL(int)
0001:0016     SYMBOL(x)
0001:0018     RPAREN
0001:0019      COLON(:)
0001:0020    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(pass)
0002:0009    NEWLINE
0002:0009     DEDENT
0002:0009    NEWLINE
""" )



def test_init_method():
    assert_parser_result(
        r"""
0001:0001    "class"(class)
0001:0007     SYMBOL(MyClass)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005 "def_init"(def_init)
0002:0014     LPAREN
0002:0016     SYMBOL(int)
0002:0020     SYMBOL(x)
0002:0022     RPAREN
0002:0023      COLON(:)
0002:0024    NEWLINE
0003:0001     INDENT
0003:0009     SYMBOL(pass)
0003:0013    NEWLINE
0003:0013     DEDENT
0003:0013    NEWLINE
0003:0013     DEDENT
0003:0013    NEWLINE
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:]
                [SYMBOL:int]
                [SYMBOL:x]
            [COLON::]
                [SYMBOL:pass]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDefInit(
            (
                (
                    PepSymbol('int'), 
                    PepSymbol('x')
                ),
            ),
            (
                PepSymbol('pass'),
            )
        ),
    )
)
""" )

def test_var_block_in_def_init():
    assert_parser_result_from_code(
        r"""
class MyClass:
    def_init():
        var:
            int self.x = 3
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:(]
            [COLON::]
                ["var":var]
                    [COLON::]
                        [EQUALS:=]
                            [SYMBOL:int]
                            [SYMBOL:self.x]
                            [INT:3]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDefInit(
            (),
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol('int'),
                            PepSymbol('self.x'),
                            PepInt('3')
                        ),
                    )
                ),
            )
        ),
    )
)
""" )


def test_def_init_with_empty_line():
    assert_parser_result_from_code(
        r"""
class MyClass:
    def_init():
        int x = 0

        int y =2
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:(]
            [COLON::]
                [EQUALS:=]
                    [SYMBOL:int]
                    [SYMBOL:x]
                    [INT:0]
                [EQUALS:=]
                    [SYMBOL:int]
                    [SYMBOL:y]
                    [INT:2]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDefInit(
            (),
            (
                PepInit(
                    PepSymbol('int'),
                    PepSymbol('x'),
                    PepInt('0')
                ), 
                PepInit(
                    PepSymbol('int'),
                    PepSymbol('y'),
                    PepInt('2')
                )
            )
        ),
    )
)
""" )


def test_var_block_with_empty_line():
    assert_parser_result_from_code(
        r"""
class MyClass:
    def_init():
        var:
            int self.x = 3

            int self.y = 4
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:(]
            [COLON::]
                ["var":var]
                    [COLON::]
                        [EQUALS:=]
                            [SYMBOL:int]
                            [SYMBOL:self.x]
                            [INT:3]
                        [EQUALS:=]
                            [SYMBOL:int]
                            [SYMBOL:self.y]
                            [INT:4]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDefInit(
            (),
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol('int'),
                            PepSymbol('self.x'),
                            PepInt('3')
                        ), 
                        PepInit(
                            PepSymbol('int'),
                            PepSymbol('self.y'),
                            PepInt('4')
                        )
                    )
                ),
            )
        ),
    )
)
""" )


def test_comments_in_init_and_var():
    assert_parser_result_from_code(
        r"""
class MyClass:
    def_init():
# ignored
        var:
        # ignored
            # ignored
# ignored
            int self.x = 3
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:(]
            [COLON::]
                ["var":var]
                    [COLON::]
                        [EQUALS:=]
                            [SYMBOL:int]
                            [SYMBOL:self.x]
                            [INT:3]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDefInit(
            (),
            (
                PepVar(
                    (
                        PepInit(
                            PepSymbol('int'),
                            PepSymbol('self.x'),
                            PepInt('3')
                        ),
                    )
                ),
            )
        ),
    )
)
""" )



def test_empty_line_in_class():
    assert_parser_result_from_code(
        r"""
class MyClass:
    def void meth( MyClass self ):
        pass

    def void meth2( MyClass self ):
        pass
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:meth]
            [LPAREN:(]
                [SYMBOL:MyClass]
                [SYMBOL:self]
            [COLON::]
                [SYMBOL:pass]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:meth2]
            [LPAREN:(]
                [SYMBOL:MyClass]
                [SYMBOL:self]
            [COLON::]
                [SYMBOL:pass]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDef(
            PepSymbol('void'),
            PepSymbol('meth'),
            ((PepSymbol('MyClass'), PepSymbol('self')),),
            (
                PepSymbol('pass'),
            )
        ), 
        PepDef(
            PepSymbol('void'),
            PepSymbol('meth2'),
            ((PepSymbol('MyClass'), PepSymbol('self')),),
            (
                PepSymbol('pass'),
            )
        )
    )
)
""" )



def test_comments_in_class():
    assert_parser_result_from_code(
        r"""
class MyClass:
# ignored
    # ignored
    def void meth( MyClass self ):
# ignored
        #ignored
        pass
        #ignored
# ignored
    # ignored

    # ignored
    def void meth2( MyClass self ):
        pass
    # ignored
# ignored
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:meth]
            [LPAREN:(]
                [SYMBOL:MyClass]
                [SYMBOL:self]
            [COLON::]
                [SYMBOL:pass]
        ["def":def]
            [SYMBOL:void]
            [SYMBOL:meth2]
            [LPAREN:(]
                [SYMBOL:MyClass]
                [SYMBOL:self]
            [COLON::]
                [SYMBOL:pass]
[EOF:]
""",
        r"""
PepClass(
    PepSymbol('MyClass'),
    (),
    (
        PepDef(
            PepSymbol('void'),
            PepSymbol('meth'),
            ((PepSymbol('MyClass'), PepSymbol('self')),),
            (
                PepSymbol('pass'),
            )
        ), 
        PepDef(
            PepSymbol('void'),
            PepSymbol('meth2'),
            ((PepSymbol('MyClass'), PepSymbol('self')),),
            (
                PepSymbol('pass'),
            )
        )
    )
)
""" )



