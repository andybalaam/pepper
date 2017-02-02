# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.builtins import *
from libpepper.environment import PepEnvironment
from libpepper.languagevalues import *
from libpepper.values import *

def test_initialisation():
    env = PepEnvironment( None )
    add_builtins( env )

    init = PepInit( PepSymbol( "int" ), PepSymbol( "i" ), PepInt( "7" ) )
    init.evaluate( env )

    value = PepSymbol( "i" )

    assert_equal( value.evaluate( env ).value, "7" )

