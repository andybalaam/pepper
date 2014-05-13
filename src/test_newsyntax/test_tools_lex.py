from nose.tools import *
from tools_lex import _simplify_lexed

@istest
def simplify_doesnt_touch_already_simple():
    assert_equals(
                         "symbol:foo ( int:3 )",
        _simplify_lexed( "symbol:foo ( int:3 )" ),
    )


@istest
def simplify_removes_extra_spaces():
    assert_equals(
                         "symbol:foo ( int:3 )",
        _simplify_lexed( "symbol:foo  ( int:3 )" ),
    )

@istest
def simplify_replaces_whitespace_with_spaces():
    assert_equals(
                         "symbol:foo ( int:3 )",
        _simplify_lexed( "symbol:foo\n( \tint:3\n )" ),
    )

@istest
def simplify_trims_outer_whitespace():
    assert_equals(
                         "symbol:foo",
        _simplify_lexed( " symbol:foo " ),
    )

@istest
def simplify_replaces_multiline_with_spaces():
    assert_equals(
                         "symbol:foo ( int:3 )",
        _simplify_lexed( """
            symbol:foo
            ( \tint:3
            )
        """ ),
    )

