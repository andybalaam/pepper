from tools_lex import *

@istest
def int():
    assert_lex( "1", "int:1" )

@istest
def string_single_quote():
    assert_lex( '"foo"', 'string:foo' )

@istest
def symbol():
    assert_lex( "foo", "symbol:foo" )

@istest
def several():
    assert_lex(
        "x(3).foo(7)",
        "symbol:x ( int:3 ) . symbol:foo ( int:7 )"
    )

