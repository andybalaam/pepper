from tools import *
from tools_ast import *

@istest
def int():
    assert_ast(
        '1',
        """
        [INT:1]
        [EOF:]
        """
    )

@istest
def two_blocks_int_int():
    assert_ast(
        '1 1',
        """
        [INT:1]
        [INT:1]
        [EOF:]
        """
    )

@istest
def string():
    assert_ast(
        '"foo"',
        """
        [STRING:foo]
        [EOF:]
        """
    )

@istest
def symbol():
    assert_ast(
        'foo',
        """
        [SYMBOL:foo]
        [EOF:]
        """
    )

@istest
def sum_of_ints():
    assert_ast(
        "1 + 2",
        """
        [PLUS:+]
            [INT:1]
            [INT:2]
        [EOF:]
        """
    )

@istest
def sum_of_symbol_and_int():
    assert_ast(
        "a + 2",
        """
        [PLUS:+]
            [SYMBOL:a]
            [INT:2]
        [EOF:]
        """
    )

@istest
def longer_sum():
    assert_ast(
        "1 + a - 2",
        """
        [PLUS:+]
            [INT:1]
            [MINUS:-]
                [SYMBOL:a]
                [INT:2]
        [EOF:]
        """
    )

@istest
def function_call_no_args():
    assert_ast(
        "foo()",
        """
        [LPAREN:(]
            [SYMBOL:foo]
        [EOF:]
        """
    )

@istest
def function_call_one_arg():
    assert_ast(
        "foo( bar )",
        """
        [LPAREN:(]
            [SYMBOL:foo]
            [SYMBOL:bar]
        [EOF:]
        """
    )

@istest
def function_call_multiple_args():
    assert_ast(
        "foo( 1, bar, 4 )",
        """
        [LPAREN:(]
            [SYMBOL:foo]
            [INT:1]
            [COMMA:,]
            [SYMBOL:bar]
            [COMMA:,]
            [INT:4]
        [EOF:]
        """
    )

@istest
def double_function_call():
    assert_ast(
        "foo( 1, bar, 4 )( 1 )",
        """
        [LPAREN:(]
            [LPAREN:(]
                [SYMBOL:foo]
                [INT:1]
                [COMMA:,]
                [SYMBOL:bar]
                [COMMA:,]
                [INT:4]
            [INT:1]
        [EOF:]
        """
    )

@istest
def double_function_call_even_if_space():
    assert_ast(
        "foo( 1, bar, 4 ) ( 1 )",
        """
        [LPAREN:(]
            [LPAREN:(]
                [SYMBOL:foo]
                [INT:1]
                [COMMA:,]
                [SYMBOL:bar]
                [COMMA:,]
                [INT:4]
            [INT:1]
        [EOF:]
        """
    )

@istest
def two_blocks_function_call_separator_bracketed_item():
    """
    two_blocks_function_call_bracketted
    This is not parsed as a double function call (like the above test)
    because there is a semi-colon separating the two blocks.
    """
    assert_ast(
        "foo( 1, bar, 4 ) ; ( 1 )",
        """
        [LPAREN:(]
            [SYMBOL:foo]
            [INT:1]
            [COMMA:,]
            [SYMBOL:bar]
            [COMMA:,]
            [INT:4]
        [SEMICOLON:;]
        [INT:1]
        [EOF:]
        """
    )

@istest
def lookup():
    assert_ast(
        'foo.bar',
        """
        [DOT:.]
            [SYMBOL:foo]
            [SYMBOL:bar]
        [EOF:]
        """
    )

@skip    # Need to make . and ( at the same level, not allow . precedence
@istest
def several():
    assert_ast(
        'x(3).foo(7)',
        ""
#        [LPAREN:(]
#            [DOT:.]
#                [LPAREN:(]
#                    [SYMBOL:x]
#                    [INT:3]
#            [INT:7]
#        [EOF:]
#        """
    )


