
from assert_parser_result import assert_parser_result
from assert_parser_result import assert_parser_result_from_code

def test_simple_initialisation():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(int)
0001:0005     SYMBOL(i)
0001:0007     EQUALS(=)
0001:0009        INT(7)
0001:0010    NEWLINE
""",
        r"""
[EQUALS:=]
    [SYMBOL:int]
    [SYMBOL:i]
    [INT:7]
""",
        r"""
EeyInit(
    EeySymbol('int'),
    EeySymbol('i'),
    EeyInt('7')
)
""" )


def test_float_initialisation():
    assert_parser_result(
        r"""
0001:0001     SYMBOL(float)
0001:0007     SYMBOL(f)
0001:0009     EQUALS(=)
0001:0011      FLOAT(7.4)
0001:0014    NEWLINE
""",
        r"""
[EQUALS:=]
    [SYMBOL:float]
    [SYMBOL:f]
    [FLOAT:7.4]
""",
        r"""
EeyInit(
    EeySymbol('float'),
    EeySymbol('f'),
    EeyFloat('7.4')
)
""" )


def test_multipart_name():
    assert_parser_result_from_code(
        r"""
int self.x = 4
""",
        r"""
[EQUALS:=]
    [SYMBOL:int]
    [SYMBOL:self.x]
    [INT:4]
""",
        r"""
EeyInit(
    EeySymbol('int'),
    EeySymbol('self.x'),
    EeyInt('4')
)
""" )


