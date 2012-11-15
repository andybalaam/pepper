# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment

from libeeyore.vals.all_values import *

def PlusEquals_increases_int_value___test():

    env = EeyEnvironment( None )
    builtins.add_builtins( env )

    EeyInit( EeySymbol('int'), EeySymbol('x'), EeyInt('7') ).evaluate( env )

    # Sanity
    assert_equal( "7", EeySymbol('x').evaluate( env ).value )

    EeyModification( EeySymbol('x'), EeyInt('3') ).evaluate( env )

    assert_equal( "10", EeySymbol('x').evaluate( env ).value )


def PlusEquals_increases_float_value___test():

    env = EeyEnvironment( None )
    builtins.add_builtins( env )

    EeyInit(
        EeySymbol('float'),
        EeySymbol('x'),
        EeyFloat('7.2')
    ).evaluate( env )

    # Sanity
    assert_equal( "7.2", EeySymbol('x').evaluate( env ).value )

    EeyModification( EeySymbol('x'), EeyFloat('0.3') ).evaluate( env )

    assert_equal( "7.5", EeySymbol('x').evaluate( env ).value )


