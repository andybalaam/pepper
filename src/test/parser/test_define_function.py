from assert_parser_result import assert_parser_result
from assert_parser_result import assert_parser_result_from_code

def test_define_function():
    assert_parser_result(
        r"""
0001:0001      "def"(def)
0001:0005     SYMBOL(int)
0001:0009     SYMBOL(myfn)
0001:0013     LPAREN
0001:0014     RPAREN
0001:0015      COLON(:)
0001:0016    NEWLINE
0002:0001     INDENT
0002:0005   "return"(return)
0002:0012        INT(1)
0002:0013    NEWLINE
0002:0013     DEDENT
0002:0013    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["def":def]
    [SYMBOL:int]
    [SYMBOL:myfn]
    [LPAREN:]
    [COLON::]
        ["return":return]
            [INT:1]
""",
        r"""
EeyDef(
    EeySymbol('int'),
    EeySymbol('myfn'),
    (),
    (
        EeyReturn(
            EeyInt('1')
        ),
    )
)
""" )


def test_define_function_with_args():
    assert_parser_result(
        r"""
0001:0001      "def"(def)
0001:0005     SYMBOL(void)
0001:0010     SYMBOL(myfn)
0001:0014     LPAREN
0001:0016     SYMBOL(int)
0001:0020     SYMBOL(x)
0001:0021      COMMA(,)
0001:0023     SYMBOL(bool)
0001:0028     SYMBOL(y)
0001:0029      COMMA(,)
0001:0031     SYMBOL(int)
0001:0035     SYMBOL(z)
0001:0037     RPAREN
0001:0038      COLON(:)
0001:0039    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(pass)
0002:0009    NEWLINE
0002:0009     DEDENT
0002:0009    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["def":def]
    [SYMBOL:void]
    [SYMBOL:myfn]
    [LPAREN:]
        [SYMBOL:int]
        [SYMBOL:x]
        [COMMA:,]
        [SYMBOL:bool]
        [SYMBOL:y]
        [COMMA:,]
        [SYMBOL:int]
        [SYMBOL:z]
    [COLON::]
        [SYMBOL:pass]
""",
        r"""
EeyDef(
    EeySymbol('void'),
    EeySymbol('myfn'),
    (
        (EeySymbol('int'), EeySymbol('x')), 
        (EeySymbol('bool'), EeySymbol('y')), 
        (EeySymbol('int'), EeySymbol('z'))
    ),
    (
        EeySymbol('pass'),
    )
)
""" )


def test_define_function_two_lines():
    assert_parser_result(
        r"""
0001:0001      "def"(def)
0001:0005     SYMBOL(void)
0001:0010     SYMBOL(myfn)
0001:0014     LPAREN
0001:0015     RPAREN
0001:0016      COLON(:)
0001:0017    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(int)
0002:0009     SYMBOL(a)
0002:0011     EQUALS(=)
0002:0013        INT(7)
0002:0014    NEWLINE
0003:0005   "return"(return)
0003:0012     SYMBOL(a)
0003:0013    NEWLINE
0003:0013     DEDENT
0003:0013    NEWLINE
0004:0001    NEWLINE
""",
        r"""
["def":def]
    [SYMBOL:void]
    [SYMBOL:myfn]
    [LPAREN:]
    [COLON::]
        [EQUALS:=]
            [SYMBOL:int]
            [SYMBOL:a]
            [INT:7]
        ["return":return]
            [SYMBOL:a]
""",
        """
EeyDef(
    EeySymbol('void'),
    EeySymbol('myfn'),
    (),
    (
        EeyInit(
            EeySymbol('int'),
            EeySymbol('a'),
            EeyInt('7')
        ), 
        EeyReturn(
            EeySymbol('a')
        )
    )
)
""" )



def test_empty_line_in_function():
    assert_parser_result_from_code(
        r"""
def int fn():
    int x = 0

    return x
""",
        r"""
["def":def]
    [SYMBOL:int]
    [SYMBOL:fn]
    [LPAREN:(]
    [COLON::]
        [EQUALS:=]
            [SYMBOL:int]
            [SYMBOL:x]
            [INT:0]
        ["return":return]
            [SYMBOL:x]
""",
        r"""
EeyDef(
    EeySymbol('int'),
    EeySymbol('fn'),
    (),
    (
        EeyInit(
            EeySymbol('int'),
            EeySymbol('x'),
            EeyInt('0')
        ), 
        EeyReturn(
            EeySymbol('x')
        )
    )
)
""" )



