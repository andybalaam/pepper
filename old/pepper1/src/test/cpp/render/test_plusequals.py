# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import PepEnvironment
from libpepper.cpp.cpprenderer import PepCppRenderer

from libpepper.vals.all_values import *

def Adding_integers_renders_as_plusequals___test():

    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    PepInit(
        PepSymbol('int'),
        PepSymbol('z'),
        PepVariable( PepType( PepInt ), "z" )
    ).evaluate( env )

    stmt = PepModification( PepSymbol('z'), PepInt('4') )

    assert_equal( "z += 4", stmt.render( env ) )


def Adding_floats_renders_as_plusequals___test():

    env = PepEnvironment( PepCppRenderer() )
    builtins.add_builtins( env )

    PepInit(
        PepSymbol('float'),
        PepSymbol('z'),
        PepVariable( PepType( PepFloat ), "z" )
    ).evaluate( env )

    stmt = PepModification( PepSymbol('z'), PepFloat('4.2') )

    assert_equal( "z += 4.2", stmt.render( env ) )


