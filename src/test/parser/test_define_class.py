from assert_parser_result import assert_parser_result

def test_calculated_type():
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


