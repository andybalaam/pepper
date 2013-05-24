# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# The Lord has made his salvation known and revealed his righteousness
# to the nations. Psalm 98 v2

from nose.tools import *

from libpepper.utils.type_is import type_is

class A:
    pass

class B:
    pass

class SonOfB(B):
    pass

a   = A()
sob = SonOfB()


def Fails_when_first_arg_is_not_a_type_but_an_int__test():
    with assert_raises( AssertionError ) as cm:
        type_is( 3, a )
    assert_regexp_matches( str( cm.exception ), "^Wrong arguments" )

def Fails_when_first_arg_is_not_a_type_but_an_instance__test():
    with assert_raises( AssertionError ):
        type_is( a, a )


def Does_nothing_when_class_matches__test():
    type_is( A, a )

def Does_nothing_when_primitive_type_matches__test():
    type_is( int, 3 )


def Throws_when_class_does_not_match__test():
    with assert_raises( AssertionError ) as cm:
        type_is( B, a )
    assert_regexp_matches( str( cm.exception ), "^type_is check failed" )
    assert_regexp_matches( str( cm.exception ), "B but found" )
    assert_regexp_matches( str( cm.exception ), "A.$" )


def Throws_when_primitive_type_does_not_match__test():
    with assert_raises( AssertionError ) as cm:
        type_is( int, "foo" )
    assert_regexp_matches( str( cm.exception ), "^type_is check failed" )
    assert_regexp_matches( str( cm.exception ), "int but found" )
    assert_regexp_matches( str( cm.exception ), "str.$" )


def Throws_on_instance_of_subclass__test():
    with assert_raises( AssertionError ) as cm:
        type_is( B, sob )
    assert_regexp_matches( str( cm.exception ), "^type_is check failed" )
    assert_regexp_matches( str( cm.exception ), "B but found" )
    assert_regexp_matches( str( cm.exception ), "SonOfB.$" )

