# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import *
from libpepper.environment import EeyEnvironment
from libpepper.languagevalues import *
from libpepper.values import *

def test_initialisation():
    env = EeyEnvironment( None )
    add_builtins( env )

    init = EeyInit( EeySymbol( "int" ), EeySymbol( "i" ), EeyInt( "7" ) )
    init.evaluate( env )

    value = EeySymbol( "i" )

    assert_equal( value.evaluate( env ).value, "7" )

