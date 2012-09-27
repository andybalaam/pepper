from assert_parser_result import assert_parser_result_from_code

def test_for_in_tuple():
    assert_parser_result_from_code(
        r"""
for int i in ( 1, 2, 3 ):
    pass
""",
        r"""
["for":for]
    [SYMBOL:int]
    [SYMBOL:i]
    [COMMA:,]
        [INT:1]
        [INT:2]
        [INT:3]
    [COLON::]
        [SYMBOL:pass]
""",
        r"""
EeyFor(
    EeySymbol('int'),
    EeySymbol('i'),
    EeyTuple(
        (
            EeyInt('1'), 
            EeyInt('2'), 
            EeyInt('3')
        )
    ),
    (
        EeySymbol('pass'),
    )
)
""" )


def test_for_init_in_range():
    assert_parser_result_from_code(
        r"""
for int i in range( 0, 4 ):
    print( i )
""",
        r"""
["for":for]
    [SYMBOL:int]
    [SYMBOL:i]
    [LPAREN:(]
        [SYMBOL:range]
        [INT:0]
        [COMMA:,]
        [INT:4]
    [COLON::]
        [LPAREN:(]
            [SYMBOL:print]
            [SYMBOL:i]
""",
        r"""
EeyFor(
    EeySymbol('int'),
    EeySymbol('i'),
    EeyFunctionCall(
        EeySymbol('range'),
        (
            EeyInt('0'), 
            EeyInt('4')
        )
    ),
    (
        EeyFunctionCall(
            EeySymbol('print'),
            (
                EeySymbol('i'),
            )
        ),
    )
)
""" )



