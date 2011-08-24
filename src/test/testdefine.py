
from nose.tools import *

from libeeyore.environment import EeyEnvironment
from libeeyore.values import EeySymbol
from libeeyore.usererrorexception import EeyUserErrorException

@raises( EeyUserErrorException )
def test_Use_an_undefined_symbol_throws():
    env = EeyEnvironment( None )
    value = EeySymbol( "mynotdef" )
    value.evaluate( env ) # Should throw

