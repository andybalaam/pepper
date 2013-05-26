# Copyright (C) 2013 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

# Wisdom, like an inheritance, is a good thing and benefits those who see
# the sun. Ecclesiastes 7 v11

from nose.tools import *

from abc import ABCMeta

from libpepper.utils.type_isinstance import type_isinstance

class A:
    pass

class B:
    __metaclass__ = ABCMeta

class SonOfB(B):
    pass

class SonOfSonOfB(SonOfB):
    pass

a      = A()
sob    = SonOfB()
sobsob = SonOfSonOfB()


def Fails_when_first_arg_is_not_a_type_but_an_int__test():
    with assert_raises( AssertionError ) as cm:
        type_isinstance( 3, a )
    assert_regexp_matches( str( cm.exception ), "^Wrong arguments" )

def Fails_when_first_arg_is_not_a_type_but_an_instance__test():
    with assert_raises( AssertionError ):
        type_isinstance( a, a )


def Does_nothing_when_class_matches__test():
    type_isinstance( A, a )

def Does_nothing_when_primitive_type_matches__test():
    type_isinstance( int, 3 )


def Throws_when_class_does_not_match__test():
    with assert_raises( AssertionError ) as cm:
        type_isinstance( B, a )
    assert_regexp_matches( str( cm.exception ), "^type_isinstance check failed" )
    assert_regexp_matches( str( cm.exception ), "B but found" )
    assert_regexp_matches( str( cm.exception ), "A.$" )


def Throws_when_primitive_type_does_not_match__test():
    with assert_raises( AssertionError ) as cm:
        type_isinstance( int, "foo" )
    assert_regexp_matches( str( cm.exception ), "^type_isinstance check failed" )
    assert_regexp_matches( str( cm.exception ), "int but found" )
    assert_regexp_matches( str( cm.exception ), "str.$" )


def Does_nothing_on_instance_of_subclass__test():
    type_isinstance( B, sob )

def Does_nothing_on_instance_of_subsubclass__test():
    type_isinstance( B, sobsob )
