from tools_lex import *

@skip
@istest
def int():
    assert_lex( "1", "int:1" )

@skip
@istest
def string_single_quote():
    assert_lex( '"foo"', 'string:foo' )

@skip
@istest
def symbol():
    assert_lex( "foo", "symbol:foo" )

@skip
@istest
def several():
    assert_lex(
        "x(3).foo(7)",
        "symbol:x ( int:3 ) . symbol:foo ( int:7 )"
    )

