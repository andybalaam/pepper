# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from assert_parser_result import assert_parser_result

def test_if():
    assert_parser_result(
        r"""
0001:0001       "if"(if)
0001:0004     SYMBOL(True)
0001:0008      COLON(:)
0001:0009    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(print)
0002:0010     LPAREN
0002:0012        INT(3)
0002:0014     RPAREN
0002:0015    NEWLINE
0002:0015     DEDENT
0002:0015    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["if":if]
    [SYMBOL:True]
    [COLON::]
        [LPAREN:]
            [SYMBOL:print]
            [INT:3]
""",
        r"""
PepIf(
    PepSymbol('True'),
    (
        PepFunctionCall(
            PepSymbol('print'),
            (
                PepInt('3'),
            )
        ),
    ),
    None
)
""" )


def test_if_function_call():
    assert_parser_result(
        r"""
0001:0001       "if"(if)
0001:0004     SYMBOL(f)
0001:0005     LPAREN
0001:0007        INT(3)
0001:0009     RPAREN
0001:0010      COLON(:)
0001:0011    NEWLINE
0002:0001     INDENT
0002:0005        INT(3)
0002:0006    NEWLINE
0002:0006     DEDENT
0002:0006    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["if":if]
    [LPAREN:]
        [SYMBOL:f]
        [INT:3]
    [COLON::]
        [INT:3]
""",
        r"""
PepIf(
    PepFunctionCall(
        PepSymbol('f'),
        (
            PepInt('3'),
        )
    ),
    (
        PepInt('3'),
    ),
    None
)
""" )



def test_if_operator():
    assert_parser_result(
        r"""
0001:0001       "if"(if)
0001:0004        INT(3)
0001:0006         GT(>)
0001:0008        INT(4)
0001:0009      COLON(:)
0001:0010    NEWLINE
0002:0001     INDENT
0002:0005        INT(3)
0002:0006    NEWLINE
0002:0006     DEDENT
0002:0006    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["if":if]
    [GT:>]
        [INT:3]
        [INT:4]
    [COLON::]
        [INT:3]
""",
        r"""
PepIf(
    PepGreaterThan(
        PepInt('3'),
        PepInt('4')
    ),
    (
        PepInt('3'),
    ),
    None
)
""" )


def test_if_operator_and_function():
    assert_parser_result(
        r"""
0001:0001       "if"(if)
0001:0004     SYMBOL(f)
0001:0005     LPAREN
0001:0007     SYMBOL(a)
0001:0009     RPAREN
0001:0011         GT(>)
0001:0013        INT(4)
0001:0014      COLON(:)
0001:0015    NEWLINE
0002:0001     INDENT
0002:0005        INT(3)
0002:0006    NEWLINE
0002:0006     DEDENT
0002:0006    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["if":if]
    [GT:>]
        [LPAREN:]
            [SYMBOL:f]
            [SYMBOL:a]
        [INT:4]
    [COLON::]
        [INT:3]
""",
        r"""
PepIf(
    PepGreaterThan(
        PepFunctionCall(
            PepSymbol('f'),
            (
                PepSymbol('a'),
            )
        ),
        PepInt('4')
    ),
    (
        PepInt('3'),
    ),
    None
)
""" )


def test_if_else():

    assert_parser_result(
        r"""
0001:0001       "if"(if)
0001:0004     SYMBOL(True)
0001:0008      COLON(:)
0001:0009    NEWLINE
0002:0001     INDENT
0002:0005        INT(1)
0002:0006    NEWLINE
0002:0006     DEDENT
0002:0006    NEWLINE
0003:0001     "else"(else)
0003:0005      COLON(:)
0003:0006    NEWLINE
0004:0001     INDENT
0004:0005        INT(0)
0004:0006    NEWLINE
0004:0006     DEDENT
0004:0006    NEWLINE
0005:0001    NEWLINE
""",
        r"""
["if":if]
    [SYMBOL:True]
    [COLON::]
        [INT:1]
    ["else":else]
    [COLON::]
        [INT:0]
""",
        r"""
PepIf(
    PepSymbol('True'),
    (
        PepInt('1'),
    ),
    (
        PepInt('0'),
    )
)""" )

