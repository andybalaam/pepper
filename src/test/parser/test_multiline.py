
from assert_parser_result import assert_parser_result

def test_multiline():
    assert_parser_result(
        r"""
0001:0001   "import"(import)
0001:0008     SYMBOL(sys)
0001:0011    NEWLINE
0002:0001     SYMBOL(print)
0002:0006     LPAREN
0002:0008     SYMBOL(sys.argv)
0002:0017     RPAREN
0002:0018    NEWLINE
""",
        r"""
["import":import]
    [SYMBOL:sys]
""",
        r"""
EeyImport('sys')
EeyFunctionCall(
    EeySymbol('print'),
    (
        EeySymbol('sys.argv'),
    )
)
""" )

