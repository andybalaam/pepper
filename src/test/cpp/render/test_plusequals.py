# Copyright (C) 2012 Andy Balaam and The Pepper Developers
# Released under the MIT License.  See the file COPYING.txt for details.

from nose.tools import *

from libpepper import builtins
from libpepper.environment import EeyEnvironment
from libpepper.cpp.cpprenderer import EeyCppRenderer

from libpepper.vals.all_values import *

def Adding_integers_renders_as_plusequals___test():

    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    EeyInit(
        EeySymbol('int'),
        EeySymbol('z'),
        EeyVariable( EeyType( EeyInt ), "z" )
    ).evaluate( env )

    stmt = EeyModification( EeySymbol('z'), EeyInt('4') )

    assert_equal( "z += 4", stmt.render( env ) )


def Adding_floats_renders_as_plusequals___test():

    env = EeyEnvironment( EeyCppRenderer() )
    builtins.add_builtins( env )

    EeyInit(
        EeySymbol('float'),
        EeySymbol('z'),
        EeyVariable( EeyType( EeyFloat ), "z" )
    ).evaluate( env )

    stmt = EeyModification( EeySymbol('z'), EeyFloat('4.2') )

    assert_equal( "z += 4.2", stmt.render( env ) )


