from nose.tools import *

from assert_parser_result import assert_parser_result
from assert_parser_result import parse

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
""",
        r"""
EeyClass(
    EeySymbol('MyClass'),
    (),
    (
        EeySymbol('pass'),
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
""",
        r"""
EeyClass(
    EeySymbol('MyClass'),
    (),
    (
        EeyInit(
            EeySymbol('int'),
            EeySymbol('x'),
            EeyInt('3')
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
""",
        r"""
EeyClass(
    EeySymbol('MyClass'),
    (),
    (
        EeyDef(
            EeySymbol('void'),
            EeySymbol('myfn'),
            (),
            (
                EeySymbol('pass'),
            )
        ),
    )
)
""" )



@raises( antlr.MismatchedTokenException )
def test_def_init_outside_class_is_an_error():
    parse( r"""
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
""",
        r"""
EeyClass(
    EeySymbol('MyClass'),
    (),
    (
        EeyDefInit(
            (
                (
                    EeySymbol('int'), 
                    EeySymbol('x')
                ),
            ),
            (
                EeySymbol('pass'),
            )
        ),
    )
)
""" )

def test_var_block_in_def_init():
    assert_parser_result(
        r"""
0001:0001    "class"(class)
0001:0007     SYMBOL(MyClass)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005 "def_init"(def_init)
0002:0014     LPAREN
0002:0015     RPAREN
0002:0016      COLON(:)
0002:0017    NEWLINE
0003:0001     INDENT
0003:0009      "var"(var)
0003:0012      COLON(:)
0003:0013    NEWLINE
0004:0001     INDENT
0004:0013     SYMBOL(int)
0004:0017     SYMBOL(self.x)
0004:0024     EQUALS(=)
0004:0026        INT(3)
0004:0027    NEWLINE
0004:0027     DEDENT
0004:0027    NEWLINE
0004:0027     DEDENT
0004:0027    NEWLINE
0004:0027     DEDENT
0004:0027    NEWLINE
0005:0001    NEWLINE
""",
        r"""
["class":class]
    [SYMBOL:MyClass]
    [COLON::]
        ["def_init":def_init]
            [LPAREN:]
            [COLON::]
                ["var":var]
                    [COLON::]
                        [EQUALS:=]
                            [SYMBOL:int]
                            [SYMBOL:self.x]
                            [INT:3]
""",
        r"""
EeyClass(
    EeySymbol('MyClass'),
    (),
    (
        EeyDefInit(
            (),
            (
                EeyVar(
                    (
                        EeyInit(
                            EeySymbol('int'),
                            EeySymbol('self.x'),
                            EeyInt('3')
                        ),
                    )
                ),
            )
        ),
    )
)
""" )



