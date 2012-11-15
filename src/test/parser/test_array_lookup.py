# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from assert_parser_result import assert_parser_result

def test_array_lookup():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(myarr)
0001:0006     LSQUBR
0001:0007        INT(1)
0001:0008     RSQUBR
0001:0009    NEWLINE
""",
        r"""
[LSQUBR:]
    [SYMBOL:myarr]
    [INT:1]
""",
        r"""
PepArrayLookup(
    PepSymbol('myarr'),
    PepInt('1')
)
""" )


def test_function_with_array_lookup():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(print)
0001:0006     LPAREN
0001:0007     SYMBOL(myarr)
0001:0012     LSQUBR
0001:0013        INT(2)
0001:0014     RSQUBR
0001:0015     RPAREN
0001:0016    NEWLINE
""",
    r"""
[LPAREN:]
    [SYMBOL:print]
    [LSQUBR:]
        [SYMBOL:myarr]
        [INT:2]
""",
    r"""
PepFunctionCall(
    PepSymbol('print'),
    (
        PepArrayLookup(
            PepSymbol('myarr'),
            PepInt('2')
        ),
    )
)
""" )


def test_array_lookup_qualified():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(a.b)
0001:0006     LSQUBR
0001:0007        INT(3)
0001:0008     RSQUBR
0001:0009    NEWLINE
""",
    r"""
[LSQUBR:]
    [SYMBOL:a.b]
    [INT:3]
""",
    r"""
PepArrayLookup(
    PepSymbol('a.b'),
    PepInt('3')
)
""" )


