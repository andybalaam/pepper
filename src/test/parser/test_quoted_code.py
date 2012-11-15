# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result

def test_quoted_sum():
    assert_parser_result(
        r"""
0001:0001    "quote"(quote)
0001:0015      COLON(:)
0001:0016    NEWLINE
0002:0001     INDENT
0002:0005     SYMBOL(x)
0002:0012       PLUS(+)
0002:0013     SYMBOL(y)
0002:0013    NEWLINE
0002:0013     DEDENT
0002:0013    NEWLINE
0003:0001    NEWLINE

""",
        r"""
["quote":quote]
    [COLON::]
        [PLUS:+]
            [SYMBOL:x]
            [SYMBOL:y]
""",
        r"""
PepQuote((PepPlus(PepSymbol('x'),PepSymbol('y')),))
""" )




