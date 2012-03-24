from assert_parser_result import assert_parser_result

def test_hello_world():
    assert_parser_result(
        r"""
0001:0001    NEWLINE
0002:0001     SYMBOL(print)
0002:0006     LPAREN
0002:0008     STRING(Hello, world!)
0002:0024     RPAREN
0002:0025    NEWLINE
0003:0001    NEWLINE
0004:0001    NEWLINE
""",
        r"""
[LPAREN:]
    [SYMBOL:print]
    [STRING:Hello, world!]
""",
        r"""
[
    EeyFunctionCall(
        EeySymbol('print'),
        (
            EeyString('Hello, world!'),
        )
    )
]
""" )

