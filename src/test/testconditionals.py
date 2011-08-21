
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.languagevalues import *
from libeeyore.values import *

def test_if_true():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( True ), ( EeyInt( "2" ), ) )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, EeyInt )
    assert_equal( ans.value, "2" )


def test_if_false():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( False ), ( EeyInt( "2" ), ) )
    assert_equal( ifv.evaluate( env ), eey_none )

