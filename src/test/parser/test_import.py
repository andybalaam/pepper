
from assert_parser_result import assert_parser_result

def test_import():
    assert_parser_result(
        r"""
0001:0001   "import"(import)
0001:0008     SYMBOL(sys)
0001:0011    NEWLINE
""",
        r"""
["import":import]
    [SYMBOL:sys]
""",
        r"""
EeyImport('sys')
""" )


