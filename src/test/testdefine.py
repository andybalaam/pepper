# Copyright (C) 2011-2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.


from nose.tools import *

from libpepper.environment import EeyEnvironment
from libpepper.values import EeySymbol
from libpepper.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_Use_an_undefined_symbol_throws():
    env = EeyEnvironment( None )
    value = EeySymbol( "mynotdef" )
    value.evaluate( env ) # Should throw

