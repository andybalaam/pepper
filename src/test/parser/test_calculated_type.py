from assert_parser_result import assert_parser_result

def test_calculated_type():
    assert_parser_result(
        r"""
0001:0001      "def"(def)
0001:0005     SYMBOL(int)
0001:0009     SYMBOL(myfn)
0001:0013     LPAREN
0001:0015     SYMBOL(fn2)
0001:0018     LPAREN
0001:0020     SYMBOL(a)
0001:0021      COMMA(,)
0001:0023     SYMBOL(b)
0001:0025     RPAREN
0001:0027     SYMBOL(cfg)
0001:0031     RPAREN
0001:0032      COLON(:)
0001:0033    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(pass)
0002:0009    NEWLINE
0002:0009     DEDENT
0002:0009    NEWLINE
0003:0001    NEWLINE
""",
        r"""
["def":def]
    [SYMBOL:int]
    [SYMBOL:myfn]
    [LPAREN:]
        [LPAREN:]
            [SYMBOL:fn2]
            [SYMBOL:a]
            [COMMA:,]
            [SYMBOL:b]
        [SYMBOL:cfg]
    [COLON::]
        [SYMBOL:pass]
""",
        r"""
EeyDef(
    EeySymbol('int'),
    EeySymbol('myfn'),
    (
        (
            EeyFunctionCall(
                EeySymbol('fn2'),
                (
                    EeySymbol('a'), 
                    EeySymbol('b')
                )
            ), 
            EeySymbol('cfg')
        ),
    ),
    (
        EeySymbol('pass'),
    )
)
""" )

