from assert_parser_result import assert_parser_result

def test_quoted_sum():
    assert_parser_result(
        r"""
0001:0001    QUOTEDCODE( x + y )
0001:0010    NEWLINE
""",
        r"""
[QUOTEDCODE: x + y ]
""",
        r"""
EeyQuote(' x + y ')
""" )

