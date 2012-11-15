# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment

from libpepper.vals.all_values import *

def PlusEquals_increases_int_value___test():

    env = PepEnvironment( None )
    builtins.add_builtins( env )

    PepInit( PepSymbol('int'), PepSymbol('x'), PepInt('7') ).evaluate( env )

    # Sanity
    assert_equal( "7", PepSymbol('x').evaluate( env ).value )

    PepModification( PepSymbol('x'), PepInt('3') ).evaluate( env )

    assert_equal( "10", PepSymbol('x').evaluate( env ).value )


def PlusEquals_increases_float_value___test():

    env = PepEnvironment( None )
    builtins.add_builtins( env )

    PepInit(
        PepSymbol('float'),
        PepSymbol('x'),
        PepFloat('7.2')
    ).evaluate( env )

    # Sanity
    assert_equal( "7.2", PepSymbol('x').evaluate( env ).value )

    PepModification( PepSymbol('x'), PepFloat('0.3') ).evaluate( env )

    assert_equal( "7.5", PepSymbol('x').evaluate( env ).value )


