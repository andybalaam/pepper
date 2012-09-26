from assert_parser_result import assert_parser_result_from_code

def test_bracketed_number():
    assert_parser_result_from_code(
        r"""
print( ( 3 ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
""",
        r"""
EeyFunctionCall(
    EeySymbol('print'),
    (
        EeyInt('3'),
    )
)
""" )


def test_double_bracketed_number():
    assert_parser_result_from_code(
        r"""
print( ( ( 3 ) ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [INT:3]
""",
        r"""
EeyFunctionCall(
    EeySymbol('print'),
    (
        EeyInt('3'),
    )
)
""" )


def test_basic_tuple():
    assert_parser_result_from_code(
        r"""
print( ( 1, 2, 3 ) )
""",
        r"""
[LPAREN:(]
    [SYMBOL:print]
    [COMMA:,]
        [INT:1]
        [INT:2]
        [INT:3]
""",
        r"""
EeyFunctionCall(
    EeySymbol('print'),
    (
        EeyTuple(
            (
                EeyInt('1'), 
                EeyInt('2'), 
                EeyInt('3')
            )
        ),
    )
)
""" )




