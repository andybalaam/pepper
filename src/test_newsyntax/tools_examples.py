from tools_lex import *

def assert_example(
    code,
    lexed,
    parsed,
    reduced,
    blocked,
    cpp,
    output
):
    assert_lex( code, lexed )
    #assert_parsed( lexed, parsed )
    #assert_reduced( parsed, reduced )

