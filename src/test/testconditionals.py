# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import EeyEnvironment
from libpepper.languagevalues import *
from libpepper.values import *

def test_if_true():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( True ), ( EeyInt( "2" ), ), None )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, EeyInt )
    assert_equal( ans.value, "2" )


def test_if_false():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( False ), ( EeyInt( "2" ), ), None )
    assert_equal( ifv.evaluate( env ), eey_none )


def test_if_with_else_true():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( True ), ( EeyInt( "2" ), ), ( EeyInt( "3" ), ) )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, EeyInt )
    assert_equal( ans.value, "2" )


def test_if_with_else_false():
    env = EeyEnvironment( None )
    ifv = EeyIf( EeyBool( False ), ( EeyInt( "2" ), ), ( EeyInt( "3" ), ) )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, EeyInt )
    assert_equal( ans.value, "3" )

