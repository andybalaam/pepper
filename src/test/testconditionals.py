# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import PepEnvironment
from libpepper.languagevalues import *
from libpepper.values import *

def test_if_true():
    env = PepEnvironment( None )
    ifv = PepIf( PepBool( True ), ( PepInt( "2" ), ), None )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, PepInt )
    assert_equal( ans.value, "2" )


def test_if_false():
    env = PepEnvironment( None )
    ifv = PepIf( PepBool( False ), ( PepInt( "2" ), ), None )
    assert_equal( ifv.evaluate( env ), pep_none )


def test_if_with_else_true():
    env = PepEnvironment( None )
    ifv = PepIf( PepBool( True ), ( PepInt( "2" ), ), ( PepInt( "3" ), ) )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, PepInt )
    assert_equal( ans.value, "2" )


def test_if_with_else_false():
    env = PepEnvironment( None )
    ifv = PepIf( PepBool( False ), ( PepInt( "2" ), ), ( PepInt( "3" ), ) )
    ans = ifv.evaluate( env )
    assert_equal( ans.__class__, PepInt )
    assert_equal( ans.value, "3" )

