from nose.tools import *

from libeeyore import builtins
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from libeeyore.vals.all_values import *

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


