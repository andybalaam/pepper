from tools_lex import *
from tools_ast import *
from tools_parse import *

def assert_example(
    code,
    lexed,
    ast,
    parsed,
    reduced,
    blocked,
    cpp,
    output
):
    assert_lex( code, lexed )
    assert_ast( code, ast )
    assert_parsed( code, parsed )
    #assert_reduced( parsed, reduced )

