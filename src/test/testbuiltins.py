
from nose.tools import *

from libeeyore.builtins import *
from libeeyore.environment import EeyEnvironment
from libeeyore.values import *

def test_true():
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( "True" )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, EeyBool )
    assert_equal( ans.value, True )


def test_false():
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( "False" )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, EeyBool )
    assert_equal( ans.value, False )

def test_len():
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( "len" )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, EeyLen )

def test_int():
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( "int" )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, EeyType )
    assert_equal( ans.value, EeyInt )

def test_bool():
    env = EeyEnvironment( None )
    add_builtins( env )

    value = EeySymbol( "bool" )
    ans = value.evaluate( env )

    assert_equal( ans.__class__, EeyType )
    assert_equal( ans.value, EeyBool )

def test_print_return_type_is_none():
    assert_equal( EeyPrint().return_type(), EeyNoneType )

def test_len_return_type_is_int():
    assert_equal( EeyLen().return_type(), EeyInt )


