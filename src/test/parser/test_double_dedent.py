from assert_parser_result import assert_parser_result

def test_double_dedent():
    assert_parser_result(
        r"""
0001:0001      "def"(def)
0001:0005     SYMBOL(type)
0001:0010     SYMBOL(myfn)
0001:0014     LPAREN
0001:0016     SYMBOL(int)
0001:0020     SYMBOL(cfg)
0001:0024     RPAREN
0001:0025      COLON(:)
0001:0026    NEWLINE
0002:0001     INDENT
0002:0005       "if"(if)
0002:0008     SYMBOL(cfg)
0002:0012         GT(>)
0002:0014        INT(0)
0002:0015      COLON(:)
0002:0016    NEWLINE
0003:0001     INDENT
0003:0009   "return"(return)
0003:0016     SYMBOL(int)
0003:0019    NEWLINE
0003:0019     DEDENT
0003:0019    NEWLINE
0004:0005     "else"(else)
0004:0009      COLON(:)
0004:0010    NEWLINE
0005:0001     INDENT
0005:0009   "return"(return)
0005:0016     SYMBOL(float)
0005:0021    NEWLINE
0005:0021     DEDENT
0005:0021    NEWLINE
0005:0021     DEDENT
0005:0021    NEWLINE
0006:0001    NEWLINE
0007:0001    NEWLINE
""", # Note the newline inserted between dedents by the lexing step
        r"""
["def":def]
    [SYMBOL:type]
    [SYMBOL:myfn]
    [LPAREN:]
        [SYMBOL:int]
        [SYMBOL:cfg]
    [COLON::]
        ["if":if]
            [GT:>]
                [SYMBOL:cfg]
                [INT:0]
            [COLON::]
                ["return":return]
                    [SYMBOL:int]
            ["else":else]
            [COLON::]
                ["return":return]
                    [SYMBOL:float]
""",
        r"""
EeyDef(
    EeySymbol('type'),
    EeySymbol('myfn'),
    (
        (
            EeySymbol('int'), 
            EeySymbol('cfg')
        ),
    ),
    (
        EeyIf(
            EeyGreaterThan(
                EeySymbol('cfg'),
                EeyInt('0')
            ),
            (
                EeyReturn(
                    EeySymbol('int')
                ),
            ),
            (
                EeyReturn(
                    EeySymbol('float')
                ),
            )
        ),
    )
)
""" )


