# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import *
from libpepper.environment import PepEnvironment
from libpepper.vals.all_values import *

def assert_defined( name, expected_class, expected_value = None ):
    env = PepEnvironment( None )
    add_builtins( env )

    value = PepSymbol( name )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, expected_class )

    if expected_value != None:
        assert_equal( ans.value, expected_value )

# Statements
def test_pass():
    assert_defined( "pass", PepPass )

# Values
def test_False():
    assert_defined( "False", PepBool, False )

def test_True():
    assert_defined( "True", PepBool, True )

# Types
def test_bool():
    assert_defined( "bool", PepType, PepBool )

def test_float():
    assert_defined( "float", PepType, PepFloat )

def test_int():
    assert_defined( "int", PepType, PepInt )

def test_string():
    assert_defined( "string", PepType, PepString )

def test_void():
    assert_defined( "void", PepType, PepVoid )

def test_type():
    assert_defined( "type", PepType, PepType )

# Functions
def test_len():
    assert_defined( "len", PepLen )

def test_len_return_type_is_int():
    assert_equal( PepLen().return_type( None, () ), PepType( PepInt ) )

def test_print():
    assert_defined( "print", PepPrint )

def test_range():
    env = PepEnvironment( None )
    add_builtins( env )

    r = PepSymbol( "range" ).evaluate( env ).call(
        (PepInt("3"), PepInt("4")), env )

    assert_equal( PepRange, r.__class__ )
    assert_equal( PepInt, r.begin.__class__ )
    assert_equal( PepInt, r.end.__class__ )
    assert_equal( "3", r.begin.value )
    assert_equal( "4", r.end.value )

def test_function_type():
    env = PepEnvironment( None )
    add_builtins( env )

    f = PepSymbol( "function" ).evaluate( env ).call(
        ( PepType( PepInt ), PepTuple( ( PepType( PepString ), ) ) ), env )

    assert_equal( PepFunctionType, f.__class__ )
    assert_equal( PepType( PepInt ), f.return_type )
    assert_equal( PepTuple, f.arg_types.__class__ )
    assert_equal( PepType( PepString ), f.arg_types.items[0] )

def test_print_return_type_is_none():
    assert_equal( PepPrint().return_type( None, () ), PepType( PepNoneType ) )

def test_implements():
    assert_defined( "implements", PepImplements )

