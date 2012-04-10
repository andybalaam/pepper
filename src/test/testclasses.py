
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


def test_Member_function_can_be_executed():
    """
    Note this test may turn out to be incorrect.  Python would respond with:
        TypeError: unbound method myfunc() must be called with X instance as
        first argument (got int instance instead)
    """

    env = EeyEnvironment( EeyCppRenderer() )

    decl = EeyClass(
        name=EeySymbol( "MyClass" ),
        base_classes=(),
        body_stmts=(
            EeyDef(
                EeyType( EeyInt ),
                EeySymbol( "myfunc" ),
                (
                    ( EeyType( EeyInt ), EeySymbol( "x" ) ),
                ),
                (
                    EeyReturn( EeySymbol( "x" ) ),
                )
            ),
        )
    )

    assert_equal( decl.render( env ), "" )

    value3 = EeyFunctionCall(
        EeySymbol( "MyClass.myfunc" ),
        (
            EeyInt( "3" ),
        )
    )

    value5 = EeyFunctionCall(
        EeySymbol( "MyClass.myfunc" ),
        (
            EeyInt( "5" ),
        )
    )

    assert_equal( value5.render( env ), "5" )



