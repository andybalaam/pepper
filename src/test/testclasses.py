
from nose.tools import *

from libeeyore.builtins import add_builtins
from libeeyore.classvalues import *
from libeeyore.environment import EeyEnvironment
from libeeyore.cpp.cppvalues import *
from libeeyore.cpp.cpprenderer import EeyCppRenderer

from eeyasserts import assert_multiline_equal

def test_Static_variable_can_be_read():
    env = EeyEnvironment( EeyCppRenderer() )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyInit( EeyType( EeyInt ), EeySymbol( "i" ), EeyInt( "7" ) ),
        )
    )

    assert_equal( decl.render( env ), "" )

    value = EeySymbol( "MyClass.i" )

    assert_equal( value.render( env ), "7" )

