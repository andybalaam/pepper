from assert_parser_result import assert_parser_result

def test_quoted_sum():
    assert_parser_result(
        r"""
0001:0001    STRING( x + y )
0001:0010    NEWLINE
""",
        r"""
[STRING: x + y ]
""",
        r"""
EeyString(' x + y ')
""" )

