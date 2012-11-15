# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libeeyore.builtins import *
from libeeyore.environment import EeyEnvironment
from libeeyore.vals.all_values import *

def assert_defined( name, expected_class, expected_value = None ):
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( name )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, expected_class )

    if expected_value != None:
        assert_equal( ans.value, expected_value )

# Statements
def test_pass():
    assert_defined( "pass", EeyPass )

# Values
def test_False():
    assert_defined( "False", EeyBool, False )

def test_True():
    assert_defined( "True", EeyBool, True )

# Types
def test_bool():
    assert_defined( "bool", EeyType, EeyBool )

def test_float():
    assert_defined( "float", EeyType, EeyFloat )

def test_int():
    assert_defined( "int", EeyType, EeyInt )

def test_string():
    assert_defined( "string", EeyType, EeyString )

def test_void():
    assert_defined( "void", EeyType, EeyVoid )

def test_type():
    assert_defined( "type", EeyType, EeyType )

# Functions
def test_len():
    assert_defined( "len", EeyLen )

def test_len_return_type_is_int():
    assert_equal( EeyLen().return_type( None, () ), EeyType( EeyInt ) )

def test_print():
    assert_defined( "print", EeyPrint )

def test_range():
    env = EeyEnvironment( None )
    add_builtins( env )

    r = EeySymbol( "range" ).evaluate( env ).call(
        (EeyInt("3"), EeyInt("4")), env )

    assert_equal( EeyRange, r.__class__ )
    assert_equal( EeyInt, r.begin.__class__ )
    assert_equal( EeyInt, r.end.__class__ )
    assert_equal( "3", r.begin.value )
    assert_equal( "4", r.end.value )

def test_print_return_type_is_none():
    assert_equal( EeyPrint().return_type( None, () ), EeyType( EeyNoneType ) )


