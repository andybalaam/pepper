
from assert_parser_result import assert_parser_result
from assert_parser_result import assert_parser_result_from_code

def test_simple_modification():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(i)
0001:0003 PLUSEQUALS(+=)
0001:0009        INT(7)
0001:0010    NEWLINE
""",
        r"""
[PLUSEQUALS:+=]
    [SYMBOL:i]
    [INT:7]
""",
        r"""
EeyModification(
    EeySymbol('i'),
    EeyInt('7')
)
""" )



def test_multipart_name():
    assert_parser_result_from_code(
        r"""
self.x += 4
""",
        r"""
[PLUSEQUALS:+=]
    [SYMBOL:self.x]
    [INT:4]
""",
        r"""
EeyModification(
    EeySymbol('self.x'),
    EeyInt('4')
)
""" )

