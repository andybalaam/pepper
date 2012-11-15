# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import PepEnvironment
from libpepper.values import PepSymbol
from libpepper.usererrorexception import PepUserErrorException

@raises( PepUserErrorException )
def test_Use_an_undefined_symbol_throws():
    env = PepEnvironment( None )
    value = PepSymbol( "mynotdef" )
    value.evaluate( env ) # Should throw

